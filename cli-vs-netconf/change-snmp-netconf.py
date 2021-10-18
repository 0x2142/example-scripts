from scrapli_netconf.driver import NetconfDriver
import xmltodict


NETCONF_GET_SNMP_SERVER = """<native xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-native">
        <snmp-server>
          <community xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-snmp"/>
        </snmp-server>
      </native>"""

NETCONF_CONFIG_SNMP_SERVER = """<config>
      <native xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-native">
        <snmp-server>
          <community xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-snmp" xmlns:nc="urn:ietf:params:xml:ns:netconf:base:1.0" nc:operation="create">
            <name>{community}</name>
            </{mode}>
          </community>
        </snmp-server>
      </native>
    </config>"""

### Step 1: Open device file, load devices

# Open device list
# CSV Format: device_IP, username, password
with open('./devices.csv', 'r') as file:
    # Read each line in the csv
    for line in file:
        # Split the line into pieces, separated by comma
        device_info = line.split(',')
        
        #  Build dictionary with device IP / authentication details
        device = {}
        # Device IP should be first value in the CSV row
        device['host'] = device_info[0]
        # Username is second value in the CSV row
        device['auth_username'] = device_info[1]
        # Password is 3rd value
        device['auth_password'] = device_info[2]
        # Don't validate host SSH key
        device['auth_strict_key'] = False

        ### Step 2: Connect to device

        # Open new connection using NetconfDriver & values from device dictionary
        print(f"Connecting to {device['host']}")
        cli = NetconfDriver(**device)
        cli.open()

        ### Step 3: Check current SNMP Configuration
        config = cli.get_config(filter_=NETCONF_GET_SNMP_SERVER)
        # Covert XML into python dictionary for easy parsing
        config_dict = xmltodict.parse(config.result)

        print("\nDevice has the following SNMP Communities configured:")

        # Search in each SNMP Config item for community string & read/write mode
        for item in config_dict['rpc-reply']['data']['native']['snmp-server']['community']:
            # RO/RW is stored as a dictionary key, with value None. Check to see which key exists
            if 'RO' in item: mode = "RO"
            if 'RW' in item: mode = "RW"
            # Print SNMP config item:
            print(f"Community: {item['name']}, Mode: {mode}")

        ### Step 4: Add new SNMP Community

        # Prompt to enter new comunity string
        print("\nPlease provide a new SNMP community:")
        new_snmp = input("> ")

        # Provide read-only or read-write
        print("\nPlease provide a mode (rw / ro):")
        new_mode = input("> ")

        # Insert values into XML template
        new_config = NETCONF_CONFIG_SNMP_SERVER.format(community=new_snmp, mode=new_mode)

        # Send config change
        response = cli.edit_config(config=new_config, target="running")
        print("Added new SNMP community")
