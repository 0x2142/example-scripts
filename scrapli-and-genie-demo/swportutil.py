import csv

import yaml
    from scrapli.driver.core import IOSXEDriver


def loadDevices():
    """ Load device inventory from config.yml """
    with open("config.yml", 'r') as config:
        devicelist = yaml.full_load(config)
    return devicelist


def connect_to_device(deviceconfig):
    """ Parse device config data & open SSH connection """
    device = {}
    device['host'] = deviceconfig['address']
    device['auth_username'] = deviceconfig['username']
    device['auth_password'] = deviceconfig['password']
    device['auth_strict_key'] = False
    conn = IOSXEDriver(**device)
    conn.open()
    return conn


def getInterfaceInfo(device):
    """ Issue 'Show Interfaces' command to device """
    resp = device.send_command("show interfaces")
    intdata = resp.genie_parse_output()
    interfaceStats = {
        'total': 0,
        'intup': 0,
        'intdown': 0,
        'intdisabled': 0,
        'intop10m': 0,
        'intop100m': 0,
        'intop1g': 0,
        'intop10g': 0,
        'intmedcop': 0,
        'intmedsfp': 0,
    }
    for iface in intdata:
        # Skip VLAN / PortChannel Interfaces
        if 'Ethernet' not in iface:
            print(f'found non-ethernet interface: {iface}')
            continue
        # Skip Management interface
        if 'GigabitEthernet0/0' in iface:
            print(f'found management interface: {iface}')
            continue
        print(f"Working on interface {iface}")
        # Count all Ethernet interfaces
        interfaceStats['total'] += 1
        # Count admin-down interfaces
        if not intdata[iface]['enabled']:
            interfaceStats['intdisabled'] += 1
        # Count not connected interfaces
        elif intdata[iface]['enabled'] and intdata[iface]['oper_status'] == 'down':
            interfaceStats['intdown'] += 1
        # Count up / connected interfaces - Then collect current speeds
        elif intdata[iface]['enabled'] and intdata[iface]['connected']:
            interfaceStats['intup'] += 1
            speed = intdata[iface]['bandwidth']
            if speed == 10_000:
                interfaceStats['intop10m'] += 1
            if speed == 100_000:
                interfaceStats['intop100m'] += 1
            if speed == 1_000_000:
                interfaceStats['intop1g'] += 1
            if speed == 10_000_000:
                interfaceStats['intop10g'] += 1
        # Count number of interfaces by media type
        try:
            media = intdata[iface]['media_type']
            if '1000BaseTX' in media:
                interfaceStats['intmedcop'] += 1
            else:
                interfaceStats['intmedsfp'] += 1
        except KeyError:
            interfaceStats['intmedsfp'] += 1
    # When complete - return int stats list
    return interfaceStats


def getSystemInfo(device):
    """ Issue 'Show Version' command to device
        Return serial number, model, current software version
    """
    resp = device.send_command("show version")
    parsed = resp.genie_parse_output()
    sysinfo = []
    sysinfo.append(parsed['version']['hostname'])
    sysinfo.append(parsed['version']['chassis'])
    sysinfo.append(parsed['version']['chassis_sn'])
    sysinfo.append(parsed['version']['version'])
    return sysinfo


def writeCSV(deviceData):
    """ Write device info to CSV file """
    with open('deviceinventory.csv', 'a') as file:
        writer = csv.writer(file)
        writer.writerow(deviceData)


def collectData(deviceConnection):
    """ Runs batch of CLI scraping / parsing """
    deviceInfo = []
    # Get device info
    sysInfo = getSystemInfo(deviceConnection)
    intInfo = getInterfaceInfo(deviceConnection)
    # Get values from returned dictonary
    intList = [x for x in intInfo.values()]
    deviceInfo = sysInfo + intList
    # Write to CSV
    writeCSV(deviceInfo)


def initCSV():
    """ Pre-fills header row of CSV file """
    header = [
        'Hostname',
        'Model',
        'Serial Number',
        'Software Version',
        'Total Interfaces',
        'Interfaces UP (Total)',
        'Interfaces DOWN (Total)',
        'Interfaces Disabled',
        'Interface Operational Speed (10M)',
        'Interface Operational Speed (100M)',
        'Interface Operational Speed (1G)',
        'Interface Operational Speed (10G)',
        'Interface Media (Copper)',
        'Interface Media (SFP)',
        ]
    writeCSV(header)


def run():
    devicelist = loadDevices()
    initCSV()
    for node in devicelist['Devices']:
        device = connect_to_device(devicelist['Devices'][node])
        collectData(device)


run()
