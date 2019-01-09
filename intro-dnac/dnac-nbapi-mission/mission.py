#!/usr/bin/env python
"""DNAC Center North-Bound API Mission - edit this file

This is your starting point for the DNAC Center North-Bound API Mission.
Edit this file to
 - retrieve network devices and modules from DNA Center
 - put them into a Python JSON object
 - write a JavaScript representation into a .js file which is formatted
   to be use with the NeXt UI Toolkit for visualization

There are a few places to edit (search for MISSION comments)
 1 Provide the HTTP method type to retrieve information
 2 Complete the URL to retrieve network devices
 3 Complete the URL to retrieve device modules
 4 Complete the URL to retrieve a count of modules

Script Dependencies:
    requests

Depencency Installation:
    $ pip install requests

Copyright (c) 2018, Cisco Systems, Inc. All rights reserved.

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

import ciscosparkapi
import json
import os
import requests
# Disable Certificate warning
try:
    requests.packages.urllib3.disable_warnings()
except:
    pass
from requests.auth import HTTPBasicAuth
import sys

# Get the absolute path for the directory where this file is located "here"
here = os.path.abspath(os.path.dirname(__file__))

# Get the absolute path for the project / repository root
project_root = os.path.abspath(os.path.join(here, '../..'))

# Extend the system path to include the project root and import the env files
sys.path.insert(0, project_root)
import env_lab      # noqa
import env_user     # noqa


# Create a Cisco Spark object
spark = ciscosparkapi.CiscoSparkAPI(access_token=env_user.SPARK_ACCESS_TOKEN)


# Details for DNA Center Platform API calls
dnac_host = env_lab.DNA_CENTER['host']
dnac_user = env_lab.DNA_CENTER['username']
dnac_pass = env_lab.DNA_CENTER['password']
dnac_headers = {'content-type': 'application/json'}

# Details for the NEXT UI File
next_data_file = 'next-data-mission.js'
next_data_file_header = '/*DO NOT EDIT - NeXt Topology file generated from DNA Center Device and Module Inventory*/\n\nvar topologyData = \n'
next_data_file_footer = '\n/*DO NOT EDIT - EOF*/\n'
next_data = {}
next_data['nodes'] = []
next_data['links'] = []
next_icon = {'Switches and Hubs': 'switch',
             'Routers': 'router',
             'Wireless Controller': 'wlc',
             'Unified AP': 'accesspoint'}


def dnac_open_session(dnac_session,
                      dnac_host,
                      dnac_headers,
                      dnac_username,
                      dnac_password):
    """DNA Center login and adding cookie to session"""
    print('DNAC Login to ' + dnac_host + ' as ' + dnac_username + ' ...')
    login_url = "https://{0}/dna/system/api/v1/auth/token".format(dnac_host)
    r = requests.post(url=login_url, auth=HTTPBasicAuth(dnac_user, dnac_pass), verify=False)
    r.raise_for_status()
    # print('DNAC Login: Response Headers: ' + str(r.headers))
    # print('DNAC Login: Response Body: ' + r.text)
    session_token_val = r.json()["Token"]
    cookies = {'X-JWT-ACCESS-TOKEN': session_token_val}
    dnac_session.cookies.update(cookies)
    print('DNAC Login: Session Cookie: ' + str(cookies))
    return r


# MISSION TODO 1: What type of HTTP method is used to retrieve information
#                 from DNA Center Platform?
def dnac_get_device_count(dnac_session, dnac_host, dnac_headers):
    """DNAC Network Device Count"""
    tmp_url = 'https://%s/dna/intent/api/v1/network-device/count' % dnac_host
    r = dnac_session.MISSION(tmp_url, verify=False, headers=dnac_headers)
    r.raise_for_status()
    # print('DNAC Response Body: ' + r.text)
    return r.json()['response']
# END MISSION SECTION


# MISSION TODO 2: Complete the URL to retrieve the Network Devices
def dnac_get_devices(dnac_session, dnac_host, dnac_headers):
    """DNAC Network Devices"""
    tmp_url = 'https://%s/dna/intent/api/v1/MISSION' % dnac_host
    r = dnac_session.get(tmp_url, verify=False, headers=dnac_headers)
    r.raise_for_status()
    # print('DNAC Response Body: ' + r.text)
    return r.json()['response']
# END MISSION SECTION


def dnac_get_host_count(dnac_session, dnac_host, dnac_headers):
    """DNAC Host Count"""
    tmp_url = 'https://%s/api/v1/host/count' % dnac_host
    r = dnac_session.get(tmp_url, verify=False, headers=dnac_headers)
    r.raise_for_status()
    # print('DNAC Response Body: ' + r.text)
    return r.json()['response']


# MISSION TODO 3: Complete the URL to retrieve the Modules about a device
def dnac_get_modules(dnac_session, dnac_host, dnac_headers, device_id):
    """DNAC Modules of a Network Device"""
    tmp_url = 'https://%s/dna/intent/api/v1/' % dnac_host
    tmp_url = tmp_url + 'network-device/MISSION?MISSION=%s' % device_id

    r = dnac_session.get(tmp_url,
                         verify=False,
                         headers=dnac_headers
                         )
    r.raise_for_status()
    # print('DNAC Response Body: ' + r.text)
    return r.json()['response']
# END MISSION SECTION


# MISSION TODO 4: Complete the URL to retrieve the number (or count) of
#                 modules for a device
def dnac_get_module_count(dnac_session, dnac_host, dnac_headers, device_id):
    """DNAC Module Count of a Network Device"""
    tmp_url = 'https://%s/dna/intent/api/v1/network-device/module/MISSION' % dnac_host
    tmp_params = {'deviceId': device_id}

    r = dnac_session.get(tmp_url,
                         verify=False,
                         headers=dnac_headers,
                         params=tmp_params)
    r.raise_for_status()
    # print('DNAC Response Body: ' + r.text)
    return r.json()['response']
# END MISSION SECTION


with requests.Session() as dnac_session:
    r = dnac_open_session(dnac_session,
                          dnac_host,
                          dnac_headers,
                          dnac_user,
                          dnac_pass)

    # Getting DNAC Device Count and Host Count verbose after login
    c = dnac_get_device_count(dnac_session, dnac_host, dnac_headers)
    print('DNAC Network Device Count: ' + str(c))
    c = dnac_get_host_count(dnac_session, dnac_host, dnac_headers)
    print('DNAC Host Count: ' + str(c))

    # Put DNAC Network devices with modules into a JSON object
    devices = dnac_get_devices(dnac_session, dnac_host, dnac_headers)
    i = 0
    for d in devices:
        c = dnac_get_module_count(dnac_session,
                                  dnac_host,
                                  dnac_headers,
                                  d['id'])
        if c > 1:
            print('Device ' + d['id'] + ' with NeXt ID ' +
                  str(i) + ' has ' + str(c) + ' modules')
            next_data['nodes'].append({'id ': i,
                                       'x': (i*20),
                                       'y': 80,
                                       'name': d['hostname'],
                                       'platform': d['platformId'],
                                       'serial': d['serialNumber'],
                                       'icon': next_icon[d['family']]})
            di = i
            i += 1
            modules = dnac_get_modules(dnac_session,
                                       dnac_host,
                                       dnac_headers,
                                       d['id'])
            for m in modules:
                next_data['nodes'].append({'id ': i,
                                           'x': (i*20),
                                           'y': 20*(i-di+1),
                                           'name': m['description'],
                                           'serial': d['serialNumber'],
                                           'icon': 'server'})
                next_data['links'].append({'source': di, 'target': i})
                i += 1

    # printing JSON representation to stdout
    print(json.dumps(next_data, indent=4, sort_keys=True))

    # writing JavaScript representation into NeXt data file
    with open(next_data_file, 'w', encoding="utf-8") as outfile:
        print('Writing NeXt UI Topology Data File')
        outfile.write(next_data_file_header)
        outfile.write(json.dumps(next_data, indent=4, sort_keys=True))
        outfile.write(next_data_file_footer)

    message = spark.messages.create(env_user.SPARK_ROOM_ID,
              files=[next_data_file],
              text='MISSION: DNA Center - I have completed the mission!')
    print(message)

    print('\n\n')
    print('Network Devices and Modules from DNA Center have been written to ' +
          next_data_file)
    print('Open next-topology.html in Chrome Browser, so see the result')
