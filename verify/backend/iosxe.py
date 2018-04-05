#!/usr/bin/env python
"""Verify the IOS XE Devices are accessible and responding.

Verify that user's provide SPARK_ACCESS_TOKEN is valid and that calls to the
Cisco Spark APIs complete successfully.


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

from netmiko import ConnectHandler, ssh_exception
from ncclient import manager, transport
import requests
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Get the absolute path for the directory where this file is located "here"
here = os.path.abspath(os.path.dirname(__file__))

# Get the absolute path for the project / repository root
project_root = os.path.abspath(os.path.join(here, "../.."))

# Extend the system path to include the project root and import the env files
if project_root not in sys.path:
    sys.path.insert(0, project_root)


import env_lab  # noqa
import env_user  # noqa


def verify() -> bool:
    """Verify access to the IOS XE Lab Devices."""
    print("==> Verifying access to the IOS XE Lab Devices for Environment.")
    print("        Environment: {}".format(env_lab.ENVIRONMENT_IN_USE))
    print("")

    devices = [env_lab.IOS_XE_1]

    # If at a DNE event, also test IOS XE 2
    if env_lab.ENVIRONMENT_IN_USE == "express":
        devices.append(env_lab.IOS_XE_2)

    for device in devices:
        print("Testing Device {}".format(device["host"]))
        # Test: Is device pingable
        response = os.system(
            "ping -c 2 {} >> iosxe_tests.txt".format(device["host"])
        )
        # and then check the response...
        if response == 0:
            pingstatus = "Ping Success"
            print("  " + pingstatus)
        else:
            pingstatus = "Ping Failed"
            print("  " + pingstatus)
            if env_lab.ENVIRONMENT_IN_USE == "express":
                return False

        # Test: SSH to device
        try:
            net_connect = ConnectHandler(
                ip=device["host"],
                username=device["username"],
                password=device["password"],
                port=device["ssh_port"],
                device_type="cisco_ios",
            )
            net_connect.disconnect()
            print("  SSH Success")
        except ssh_exception.NetMikoTimeoutException:
            print("  SSH Failed")
            return False

        # Test: Is NETCONF running
        try:
            with manager.connect(
                host=device["host"],
                port=device["netconf_port"],
                username=device["username"],
                password=device["password"],
                hostkey_verify=False,
            ) as m:  # noqa
                print("  NETCONF Success")
        except transport.errors.SSHError:
            print("  NETCONF Failed")
            return False

        # Test: Is RESTCONF running
        url = "https://{}:{}/restconf/data/ietf-interfaces:interfaces"
        url = url.format(device["host"], device["restconf_port"])
        r = requests.get(
            url, auth=(device["username"], device["password"]), verify=False
        )
        if r.status_code == 200:
            print("  RESTCONF Success")
        else:
            print("  RESTCONF Failed")
            return False

        print("Tests complete.\n")

    return True


if __name__ == "__main__":
    verify()
