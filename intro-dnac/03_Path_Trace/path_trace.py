import requests
import json
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

"""   
    This code snippet will initiate a path trace between a switch 
    in our network {source_ip} and our fusion router {dest_ip}
"""


def get_auth_token():
    """
    Building out Auth request. Using requests.post to make a call to the Auth Endpoint
    """
    url = 'https://{}/dna/system/api/v1/auth/token'.format(DNAC_URL)                      # Endpoint URL
    hdr = {'content-type' : 'application/json'}                                           # Define request header
    resp = requests.post(url, auth=HTTPBasicAuth(DNAC_USER, DNAC_PASS), headers=hdr)      # Make the POST Request
    token = resp.json()['Token']                                                          # Retrieve the Token
    return token    # Create a return statement to send the token back for later use


def get_device_list():
    """
    Building out function to retrieve list of devices. Using requests.get to make a call to the network device Endpoint
    """
    token = get_auth_token() # Get Token
    url = "https://{}/api/v1/network-device/1/10".format(DNAC_URL)
    hdr = {'x-auth-token': token, 'content-type' : 'application/json'}
    resp = requests.get(url, headers=hdr)  # Make the Get Request
    device_list = resp.json()
    print("{0:25}{1:25}{2:30}".format("hostname", "mgmt IP", "Type"))
    for device in device_list['response']:
        print("{0:25}{1:25}{2:30}".format(device['hostname'], device['managementIpAddress'], device['type']))
    initiate_path_trace(token) # initiate path trace


def initiate_path_trace(token):
    """
    This function will take 2 inputs from the user and initiate the specified trace
    """
    src_ip = str(input("Enter Source IP (cat9k switch):"))
    dest_ip = str(input("Enter Destination IP (asr router):"))
    param = {
        'destIP': dest_ip,
        'periodicRefresh': False,
        'sourceIP': src_ip
    }
    url = "https://{}/api/v1/flow-analysis".format(DNAC_URL)
    header = {'content-type': 'application/json', 'x-auth-token': token}
    path_response = requests.post(url, data=json.dumps(param), headers=header)
    path_json = path_response.json()
    flow_id = path_json['response']['flowAnalysisId']
    print("Path Trace Initiated! Path ID --> ", flow_id)
    print("Retrieving Path Trace Results.... ")
    retrieve_pt_results(flow_id, token)


def retrieve_pt_results(flow_id, token):
    url = "https://{}/api/v1/flow-analysis/{}".format(DNAC_URL, flow_id)
    hdr = {'x-auth-token': token, 'content-type' : 'application/json'}
    path_result = requests.get(url, headers=hdr)
    print(json.dumps(path_result.json(), indent=4, sort_keys=True))


if __name__ == "__main__":
    get_device_list()
