#!/usr/bin/env python
"""This script clears the IP configuration on GigabitEthernet2 on 2 devices.

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
from netconf_functions import check_ip, clear_ip


# Get the absolute path for the directory where this file is located "here"
here = os.path.abspath(os.path.dirname(__file__))

# Get the absolute path for the project / repository root
project_root = os.path.abspath(os.path.join(here, "../.."))


# Extend the system path to include the project root and import the env files
sys.path.insert(0, project_root)
import env_lab  # noqa

# Create a list of devices to query
devices = [
    {"conn": env_lab.IOS_XE_1, "ip": "172.16.255.1", "prefix": "24"},
    {"conn": env_lab.IOS_XE_2, "ip": "172.16.255.2", "prefix": "24"},
]

# Step 1: Query the devices for the current interface configuration.
print("Checking the current IP configuration on GigabitEthernet2 on devices")

# Query both devices for current interface configuration
for device in devices:
    check_ip(device)


# Step 2: Configure the IP addresses for GigabitEthernet2 on the devices
# Create an XML configuration template for openconfig-interfaces
print("Attempting to clear GigabitEthernet2 IP addressing")

# Configure GigabitEthernet2 IP on each device
for device in devices:
    clear_ip(device)

# Step 3: Print updated IP addresses on devices
print(
    "Re-Checking the current IP configuration on GigabitEthernet2 on devices"
)
# Query both devices for current interface configuration
for device in devices:
    check_ip(device)
