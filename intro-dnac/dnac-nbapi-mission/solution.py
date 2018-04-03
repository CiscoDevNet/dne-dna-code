#!/usr/bin/env python
"""DNAC Center North-Bound API Mission - Sample Solution

This is a sample solution for the DNAC Center North-Bound API Mission. The
script
 - retrieves network devices and modules from DNA Cener,
 - puts them into a ptyhon JSON object
 - writes a JavaScript representation into a .js file which is formatted
   to be use with the NeXt UI Toolkit for visualization

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

import json
import os
from pprint import pprint
import requests
# Disable Certificate warning
try:
  requests.packages.urllib3.disable_warnings()
except:
  pass

from requests.auth import HTTPBasicAuth
import sys

import ciscosparkapi


# Get the absolute path for the directory where this file is located "here"
here = os.path.abspath(os.path.dirname(__file__))

# Get the absolute path for the project / repository root
project_root = os.path.abspath(os.path.join(here, "../.."))


# Extend the system path to include the project root and import the env files
sys.path.insert(0, project_root)
import env_lab      # noqa
import env_user     # noqa

dnac_host=env_lab.DNA_CENTER["host"]
dnac_user=env_lab.DNA_CENTER["username"]
dnac_pass=env_lab.DNA_CENTER["password"]
dnac_headers={'content-type': 'application/json'}

next_data_file='next-data.js'
next_data_file_header='/*DO NOT EDIT - NeXt Topology file generated from DNA Center Device and Module Inventory*/\n\nvar topologyData = \n'
next_data_file_footer='\n/*DO NOT EDIT - EOF*/\n'
next_data = {}
next_data['nodes'] = []
next_data['links'] = []
next_icon = {'Switches and Hubs':'switch', 'Routers':'router'}

# create spark session object
spark = ciscosparkapi.CiscoSparkAPI(access_token=env_user.SPARK_ACCESS_TOKEN)
print("Oh yeah... I'm also connected to Cisco Spark as:")
print(spark.people.me())
print("...and I'm posting things to the following Spark Room:")
print(spark.rooms.get(env_user.SPARK_ROOM_ID))

def dnac_open_session(dnac_session, dnac_host, dnac_headers, dnac_username, dnac_password):

    # DNAC Login request to obtain session cookie
    print('DNAC Login to ' + dnac_host + ' as ' + dnac_username + ' ...')
    dnac_auth_api='https://%s/api/system/v1/auth/login' % dnac_host
    r = dnac_session.get(dnac_auth_api, verify=False, headers=dnac_headers, auth=HTTPBasicAuth(dnac_username, dnac_password))
    r.raise_for_status()
    print('DNAC Login: Response Headers: ' + str(r.headers))
    print('DNAC Login: Response Body: ' + r.text)

    # extract cookie from login response headers and add to session object
    session_token_val = ((r.headers['Set-Cookie']).split('=')[1]).split(';')[0]
    # session_token_val = r.json()["Token"]

    cookies = { "X-JWT-ACCESS-TOKEN" : session_token_val }
    dnac_session.cookies.update(cookies)
    print('DNAC Login: Session Cookie : ' + str(cookies))

    return r

def dnac_get_device_count(dnac_session, dnac_host, dnac_headers):
    """DNAC Network Device Count"""
    tmp_url = 'https://%s/api/v1/network-device/count' % dnac_host
    r = dnac_session.get(tmp_url, verify=False, headers=dnac_headers)
    r.raise_for_status()
    # print('DNAC Response Body: ' + r.text)
    return r.json()['response']

def dnac_get_devices(dnac_session, dnac_host, dnac_headers):
    """DNAC Network Devices"""
    tmp_url = 'https://%s/api/v1/network-device' % dnac_host
    r = dnac_session.get(tmp_url, verify=False, headers=dnac_headers)
    r.raise_for_status()
    # print('DNAC Response Body: ' + r.text)
    return r.json()['response']

def dnac_get_host_count(dnac_session, dnac_host, dnac_headers):
    """DNAC Host Count"""
    tmp_url = 'https://%s/api/v1/host/count' % dnac_host
    r = dnac_session.get(tmp_url, verify=False, headers=dnac_headers)
    r.raise_for_status()
    # print('DNAC Response Body: ' + r.text)
    return r.json()['response']

def dnac_get_module_count(dnac_session, dnac_host, dnac_headers, device_id):
    """DNAC Module Count of a Network Device"""
    tmp_url = 'https://%s/api/v1/network-device/module/count' % dnac_host
    tmp_params = {'deviceId' : device_id}

    r = dnac_session.get(tmp_url, verify=False, headers=dnac_headers, params=tmp_params)
    r.raise_for_status()
    # print('DNAC Response Body: ' + r.text)
    return r.json()['response']

def dnac_get_modules(dnac_session, dnac_host, dnac_headers, device_id):
    """DNAC Modules of a Network Device"""
    tmp_url = 'https://%s/api/v1/network-device/module' % dnac_host
    tmp_params = {'deviceId' : device_id}

    r = dnac_session.get(tmp_url, verify=False, headers=dnac_headers, params=tmp_params)
    r.raise_for_status()
    # print('DNAC Response Body: ' + r.text)
    return r.json()['response']



with requests.Session() as dnac_session:
    r = dnac_open_session(dnac_session, dnac_host, dnac_headers, dnac_user, dnac_pass)

    # Getting DNAC Device Count and Host Count verbose after login
    c = dnac_get_device_count(dnac_session, dnac_host, dnac_headers)
    print('DNAC Network Device Count: ' + str(c))
    c = dnac_get_host_count(dnac_session, dnac_host, dnac_headers)
    print('DNAC Host Count: ' + str(c))

    # Put DNAC Network devices with modules into a JSON object
    devices = dnac_get_devices(dnac_session, dnac_host, dnac_headers)
    i = 0
    for d in devices:
        c = dnac_get_module_count(dnac_session, dnac_host, dnac_headers, d['id'])
        if c > 1:
            print('Device ' + d['id'] + ' with NeXt ID '+str(i)+' has '+str(c)+' modules')

            next_data['nodes'].append({'id ': i,
                             'x': (i*20),
                             'y': 80,
                             'name': d['hostname'],
                             'platform': d['platformId'],
                             'serial': d['serialNumber'],
                             'icon':next_icon[d['family']]})
            di = i
            i += 1
            modules=dnac_get_modules(dnac_session, dnac_host, dnac_headers, d['id'])
            for m in modules:
                next_data['nodes'].append({'id ': i,
                                 'x': (i*20),
                                 'y': 20*(i-di+1),
                                 'name': m['partNumber'],
                                 'serial': d['serialNumber'],
                                 'icon':'server'})
                next_data['links'].append({'source': di, 'target': i})
                i += 1

    pprint(json.dumps(next_data))

    # writing JavaScript representation into NeXt data file
    with open(next_data_file, 'w', encoding="utf-8") as outfile:
        print('Writing NeXt UI Topology Data File')
        outfile.write(next_data_file_header)
        outfile.write(json.dumps(next_data))
        outfile.write(next_data_file_footer)
