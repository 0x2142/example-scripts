"""
Requires scrapli module:
pip install scrapli
"""

from scrapli.driver.core import IOSXEDriver

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

        # Open new connection using IOSXEDriver & values from device dictionary
        print(f"Connecting to {device['host']}")
        cli = IOSXEDriver(**device)
        cli.open()

        ### Step 3: Check current SNMP Configuration

        # Request current SNMP config
        get_snmp = cli.send_command("show run | inc snmp")

        # Get the CLI output result, then split it into individual lines
        config_list = get_snmp.result.splitlines()

        print("\nDevice has the following SNMP Communities configured:")
        # Check each line returned from the CLI
        for config in config_list:
            # Only look for config lines that contain "community"
            if "community" in config:
                # Split the line of config into a list, separated by spaces
                snmp = config.split(" ")
                # Print each SNMP community
                print(f"Community: {snmp[2]}, Mode: {snmp[3]}")


        ### Step 4: Add new SNMP Community

        # Prompt to enter new comunity string
        print("\nPlease provide a new SNMP community:")
        new_snmp = input("> ")

        # Provide read-only or read-write
        print("\nPlease provide a mode (rw / ro):")
        new_mode = input("> ")

        # Send config change
        cli.send_config(f"snmp-server community {new_snmp} {new_mode} ")
        print("Added new SNMP community")
