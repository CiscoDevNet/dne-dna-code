"""Set the Environment Information Needed to Access Your Lab!

The provided sample code in this repository will reference this file to get the
information needed to connect to your lab backend.  You provide this info here
once and the scripts in this repository will access it as needed by the lab.


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


# User Input

# Please select the lab environment that you will be using today
#     sandbox - Cisco DevNet Always-On / Reserved Sandboxes
#     express - Cisco DevNet Express Lab Backend
#     custom  - Your Own "Custom" Lab Backend
ENVIRONMENT_IN_USE = "sandbox"

# Custom Lab Backend
DNA_CENTER = {
    "host": "",
    "username": "",
    "password": ""
}

# End User Input


# Set the 'Environment Variables' based on the lab environment in use
if ENVIRONMENT_IN_USE == "sandbox":
    DNA_CENTER = {
        "host": "sandboxdnac2.cisco.com",
        "username": "dnacdev",
        "password": "D3v93T@wK!"
    }

    # Values for the Always On IOS XE Sandbox
    IOS_XE_1 = {
        "host": "ios-xe-mgmt.cisco.com",
        "username": "developer",
        "password": "C1sco12345",
        "netconf_port": 10000,
        "restconf_port": 9443,
        "ssh_port": 8181
    }

    # Values for the Reservable IOS XE Sandbox
    IOS_XE_2 = {
        "host": "10.10.20.48",
        "username": "developer",
        "password": "C1sco12345",
        "netconf_port": 830,
        "restconf_port": 443,
        "ssh_port": 22
    }

    # Values for the Always On NX-OS Sandbox
    NXOS_1 = {
        "host": "sbx-nxos-mgmt.cisco.com",
        "username": "admin",
        "password": "Admin_1234!",
        "netconf_port": 10000,
        "restconf_port": 443,
        "nxapi_port": 80,
        "ssh_port": 8181
    }

elif ENVIRONMENT_IN_USE == "express":
    DNA_CENTER = {
        "host": "sandboxdnac2.cisco.com",
        "port": 443,
        "username": "dnacdev",
        "password": "D3v93T@wK!"
    }

    NFVIS_SERVER = {
        "host": "198.18.134.46",
        "port": 443,
        "username": "admin",
        "password": "C1sco12345_"
    }

    # Values for the CSR1 from the dCloud Pod
    IOS_XE_1 = {
        "host": "198.18.134.11",
        "username": "admin",
        "password": "C1sco12345",
        "netconf_port": 830,
        "restconf_port": 443,
        "ssh_port": 22
    }

    # Values for the CSR2 from the dCloud Pod
    IOS_XE_2 = {
        "host": "198.18.134.12",
        "username": "admin",
        "password": "C1sco12345",
        "netconf_port": 830,
        "restconf_port": 443,
        "ssh_port": 22
    }

    # Values for the Always On NX-OS Sandbox
    NXOS_1 = {
        "host": "sbx-nxos-mgmt.cisco.com",
        "username": "admin",
        "password": "Admin_1234!",
        "netconf_port": 10000,
        "restconf_port": 443,
        "nxapi_port": 80,
        "ssh_port": 8181
    }
