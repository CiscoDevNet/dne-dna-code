#!/usr/bin/env python
"""Verify the NFVIS Device is accessible and responding.

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

def nvfis_getgcred():
    login = env_lab.NFVIS_SERVER['username']
    password = env_lab.NFVIS_SERVER['password']
    url = "https://" + env_lab.NFVIS_SERVER['host']
    nip = env_lab.NFVIS_SERVER['host']
    return nip, url, login, password

def nfv_get_networks_configuration(s, url):
    u = url + '/api/config/networks?deep'
    networks_configuration = s.get(u)
    return networks_configuration

def verify() -> bool:
    """Verify access to the NFVIS Device."""
    print("==> Verifying access to the NFVIS Device Environment.")

    nip, url, login, password = nvfis_getgcred()
    s = requests.Session()
    s.auth = (login, password)
    s.headers = ({'Content-type': 'application/vnd.yang.data+json', 'Accept': 'application/vnd.yang.data+json'})
    s.verify = False

    # Test: Is device pingable
    response = os.system(
        "ping -c 2 {} >> nfvis_tests.txt".format(nip)
    )
    # and then check the response...
    if response == 0:
        pingstatus = "Ping Success"
        print("  " + pingstatus)
    else:
        pingstatus = "Ping Failed"
        print("  " + pingstatus)
        return False
    
    # Test: Is the REST API running
    r = nfv_get_networks_configuration(s, url)
    if r.status_code == 200:
        print("  REST API Success")
    else:
        print("  REST API Failed")
        return False
    
    print("Tests complete.\n")

    return True


if __name__ == "__main__":
    verify()
