import requests
import json

URL = "https://api.meraki.com/api/v1"

APIKEY = {"X-Cisco-Meraki-API-Key": "<INSERT MERAKI API KEY>"}


def getOrgID():
    """
    Query Meraki API for which Organizations we have access to & return Org ID
    """
    queryURL = URL + "/organizations"
    response = requests.get(queryURL, headers=APIKEY)
    orgID = json.loads(response.text)[0]["id"]
    return orgID

def getNetworks(orgID):
    """
    Use Organization ID to pull list of networks we have access to
    """
    queryURL = URL + f"/organizations/{orgID}/networks"
    response = requests.get(queryURL, headers=APIKEY)
    data = json.loads(response.text)
    networkList = []
    for network in data:
        networkList.append(network["id"])
    return networkList

def getClients(orgID, networkList):
    """
    Query clients for each network, return client list
    """
    clientCount = {}
    total = 0
    # Query Parameters: Return up to 100 devices seen in the past 43,200 seconds (30 days)
    q = {"perPage": "100",
         "timespan": "43200"}
    for network in networkList:
        # Query clients for each network
        queryURL = URL + f"/networks/{network}/clients"
        response = requests.get(queryURL, params=q, headers=APIKEY)
        data = json.loads(response.text)
        # Grab client OS from each device & append to clientCount dictionary
        for client in data:
            try:
                clientCount[client["os"]] += 1
            except KeyError:
                clientCount[client["os"]] = 1
            except TypeError:
                continue
            total += 1
    # Append final count of all devices & return dict
    clientCount["Total Devices"] = total
    return clientCount

def printReport(clientOS):
    """
    Print final output to terminal
    """
    print("Count of clients by operating system:")
    for OS in clientOS:
        print(f"{OS}: {clientOS[OS]}")

if __name__ == '__main__':
    orgID = getOrgID()
    networkList = getNetworks(orgID)
    clientOS = getClients(orgID, networkList)
    printReport(clientOS)
