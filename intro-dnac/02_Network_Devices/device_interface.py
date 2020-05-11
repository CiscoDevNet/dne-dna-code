import requests
from requests.auth import HTTPBasicAuth
import os
import sys

# Get the absolute path for the directory where this file is located "here"
here = os.path.abspath(os.path.dirname(__file__))

# Get the absolute path for the project / repository root
project_root = os.path.abspath(os.path.join(here, "../.."))

# Extend the system path to include the project root and import the env files
sys.path.insert(0, project_root)

import env_lab

DNAC_URL = env_lab.DNA_CENTER["host"]
DNAC_USER = env_lab.DNA_CENTER["username"]
DNAC_PASS = env_lab.DNA_CENTER["password"]


def get_device_list():
    """
    Building out function to retrieve list of devices. Using requests.get to make a call to the network device Endpoint
    """
    global token
    token = get_auth_token() # Get Token
    url = "https://{}/api/v1/network-device".format(DNAC_URL)
    hdr = {'x-auth-token': token, 'content-type' : 'application/json'}
    resp = requests.get(url, headers=hdr)  # Make the Get Request
    device_list = resp.json()
    get_device_id(device_list)


def get_device_id(device_json):
    for device in device_json['response']: # Loop through Device List and Retreive DeviceId
        print("Fetching Interfaces for Device Id ----> {}".format(device['id']))
        print('\n')
        get_device_int(device['id'])
        print('\n')


def get_device_int(device_id):
    """
    Building out function to retrieve device interface. Using requests.get to make a call to the network device Endpoint
    """
    url = "https://{}/api/v1/interface".format(DNAC_URL)
    hdr = {'x-auth-token': token, 'content-type' : 'application/json'}
    querystring = {"macAddress": device_id} # Dynamically build the querey params to get device spefict Interface info
    resp = requests.get(url, headers=hdr, params=querystring)  # Make the Get Request
    interface_info_json = resp.json()
    print_interface_info(interface_info_json)


def print_interface_info(interface_info):
    print("{0:42}{1:17}{2:12}{3:18}{4:17}{5:10}{6:15}".
          format("portName", "vlanId", "portMode", "portType", "duplex", "status", "lastUpdated"))
    for int in interface_info['response']:
        print("{0:42}{1:10}{2:12}{3:18}{4:17}{5:10}{6:15}".
              format(str(int['portName']),
                     str(int['vlanId']),
                     str(int['portMode']),
                     str(int['portType']),
                     str(int['duplex']),
                     str(int['status']),
                     str(int['lastUpdated'])))


def get_auth_token():
    """
    Building out Auth request. Using requests.post to make a call to the Auth Endpoint
    """
    url = 'https://{}/dna/system/api/v1/auth/token'.format(DNAC_URL)       # Endpoint URL
    resp = requests.post(url, auth=HTTPBasicAuth(DNAC_USER, DNAC_PASS))  # Make the POST Request
    token = resp.json()['Token']    # Retrieve the Token from the returned JSONhahhah
    return token    # Create a return statement to send the token back for later use


if __name__ == "__main__":
    get_device_list()

