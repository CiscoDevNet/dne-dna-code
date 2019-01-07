#!/usr/bin/env python
"""DNAv3 - DNAC Northbound API - Hands on exercise 01
In this exercise we create helper functions to get an auth token
from DNAC - get_auth_token() and also get_url(), create_url() and
list_network_devices() to get a list of all network devices managed
by DNA Center. In the main function we extract some data we find useful
and pretty print the result.

Copyright (c) 2018 Cisco and/or its affiliates.

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

import os
import sys
import json
import requests
from requests.auth import HTTPBasicAuth
requests.packages.urllib3.disable_warnings()

# Get the absolute path for the directory where this file is located "here"
here = os.path.abspath(os.path.dirname(__file__))

# Get the absolute path for the project / repository root
project_root = os.path.abspath(os.path.join(here, "../.."))


# Extend the system path to include the project root and import the env files
sys.path.insert(0, project_root)
import env_lab      # noqa
#import env_user     # noqa

DNAC = env_lab.DNA_CENTER['host']
DNAC_USER = env_lab.DNA_CENTER['username']
DNAC_PASSWORD = env_lab.DNA_CENTER['password']
DNAC_PORT = env_lab.DNA_CENTER['port']

# -------------------------------------------------------------------
# Helper functions
# -------------------------------------------------------------------


def get_auth_token(controller_ip=DNAC, username=DNAC_USER, password=DNAC_PASSWORD):
    """ Authenticates with controller and returns a token to be used in subsequent API invocations
    """
    login_url = "https://{0}/dna/system/api/v1/auth/token".format(controller_ip, DNAC_PORT)
    result = requests.post(url=login_url, auth=HTTPBasicAuth(DNAC_USER, DNAC_PASSWORD), verify=False)
    result.raise_for_status()

    token = result.json()["Token"]
    return {
        "controller_ip": controller_ip,
        "token": token
    }


def create_url(path, controller_ip=DNAC):
    """ Helper function to create a DNAC API endpoint URL
    """
    return "https://%s/dna/intent/api/v1/%s" % (controller_ip, path)


def get_url(url):
    url = create_url(path=url)
    print(url)
    token = get_auth_token()
    headers = {'X-auth-token' : token['token']}
    try:
        response = requests.get(url, headers=headers, verify=False)
    except requests.exceptions.RequestException as cerror:
        print("Error processing request", cerror)
        sys.exit(1)

    return response.json()


def list_network_devices():
    return get_url("network-device")


if __name__ == "__main__":
    response = list_network_devices()
    print("{0:42}{1:17}{2:12}{3:18}{4:12}{5:16}{6:15}".
        format("hostname","mgmt IP","serial",
        "platformId","SW Version","role","Uptime"))

    for device in response['response']:
        uptime = "N/A" if device['upTime'] is None else device['upTime']
        print("{0:42}{1:17}{2:12}{3:18}{4:12}{5:16}{6:15}".
            format(device['hostname'],
                    device['managementIpAddress'],
                    device['serialNumber'],
                    device['platformId'],
                    device['softwareVersion'],
                    device['role'],uptime))
