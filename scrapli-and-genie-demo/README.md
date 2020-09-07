# Scrapli & Cisco Genie Demo

This is an example script that makes use of Scrapli & Cisco genie to parse CLI output from an IOS-XE device.

The purpose of this script is to:
1. Connect to one or more devices (Specified in config.yml)
2. Pull a 'show version' & 'show interfaces' using Scrapli
3. Use Genie to parse the output
4. Collect stats on total ports, used ports, port speed / media types, etc
5. Write out this data to a spreadsheet

## Usage

`config.yml` - This file contains a list of devices. Specify the hostname, username, and password for each device. Note: device type is not currently used

`swportutil.py` - After filling in the config file, run this script to collect data from each device specified in config.yml

Only two dependencies are required, as specified in requirements.txt:
1. scrapli
2. scrapli[genie]