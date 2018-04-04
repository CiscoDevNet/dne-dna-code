#!/usr/bin/env python
"""Verify the Cisco DNA Center APIs are accessible and responding.

Verify that DNA Center Sanbox Northbound APIs are accessible and
responding with data.


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
import requests
# Disable Certificate warning
try:
    requests.packages.urllib3.disable_warnings()
except:
    pass

from requests.auth import HTTPBasicAuth

# Get the absolute path for the directory where this file is located "here"
here = os.path.abspath(os.path.dirname(__file__))

# Get the absolute path for the project / repository root
project_root = os.path.abspath(os.path.join(here, "../.."))

# Extend the system path to include the project root and import the env files
if project_root not in sys.path:
    sys.path.insert(0, project_root)

import env_lab  # noqa


def dnac_get_device_count(dnac_session, dnac_host, dnac_headers):
    """DNAC Network Device Count"""
    tmp_url = 'https://%s/api/v1/network-device/count' % dnac_host
    r = dnac_session.get(tmp_url, verify=False, headers=dnac_headers)
    r.raise_for_status()
    return r.json()['response']


def dnac_get_host_count(dnac_session, dnac_host, dnac_headers):
    """DNAC Host Count"""
    tmp_url = 'https://%s/api/v1/host/count' % dnac_host
    r = dnac_session.get(tmp_url, verify=False, headers=dnac_headers)
    r.raise_for_status()
    # print('DNAC Response Body: ' + r.text)
    return r.json()['response']


def verify() -> bool:
    """Verify access to the Cisco DNAC APIs."""
    print('\n\n==> Verifying access to the Cisco DNA Center Northbound APIs')

    # Verify env_lab is accessible and complete for DNAC
    if not env_lab.DNA_CENTER['host']:
        print('FAILED: You must provide DNAC hostname in the env_lab.py file.')
        return False
    if not env_lab.DNA_CENTER['username']:
        print('FAILED: You must provide DNAC username in the env_lab.py file.')
        return False
    if not env_lab.DNA_CENTER['password']:
        print('FAILED: You must provide DNAC password in the env_lab.py file.')
        return False

    dnac_host = env_lab.DNA_CENTER['host']
    dnac_user = env_lab.DNA_CENTER['username']
    dnac_pass = env_lab.DNA_CENTER['password']
    dnac_headers = {'content-type': 'application/json'}

    # Verify DNA Center login
    with requests.Session() as dnac_session:
        try:
            dnac_auth_api='https://%s/api/system/v1/auth/login' % dnac_host
            r = dnac_session.get(dnac_auth_api,
                                 verify=False,
                                 headers=dnac_headers,
                                 auth=HTTPBasicAuth(dnac_user, dnac_pass))
            r.raise_for_status()
            session_token_val = ((r.headers['Set-Cookie']).split('=')[1]).split(';')[0]
            cookies = {"X-JWT-ACCESS-TOKEN" : session_token_val}
            dnac_session.cookies.update(cookies)
        except:
            print('FAILED: Not able to login to DNA Center at ' + dnac_host)
            return False
        else:
            print('You are connected to to DNA Center at ' + dnac_host)

        # Verify DNA Center inventory has some network devices and hosts
        try:
            c = dnac_get_device_count(dnac_session, dnac_host, dnac_headers)
            h = dnac_get_host_count(dnac_session, dnac_host, dnac_headers)
        except:
            print('FAILED: No host and device invetory in DNA Center')
            return False
        else:
            print('DNA Center Network Device Count: ' + str(c))
            print('DNA Center Host Count: ' + str(h))
            if c <= 0 or h <=0:
                print('FAILED: No host and device invetory in DNA Center')
                return False

    return True


if __name__ == '__main__':
    verify()
