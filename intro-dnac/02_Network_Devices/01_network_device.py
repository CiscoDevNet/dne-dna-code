#!/usr/bin/env python
from __future__ import print_function
import sys
import json
from util import get_url

def list_single_device(ip):
    return get_url("network-device/ip-address/%s" % ip)

def list_network_devices():
    return get_url("network-device")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        response = list_single_device(sys.argv[1])
        print(json.dumps(response, indent=2))
    else:
        response = list_network_devices()
        print("{0:42}{1:17}{2:12}{3:18}{4:12}{5:16}{6:15}".
                  format("hostname","mgmt IP","serial",
                         "platformId","SW Version","role","Uptime"))

        for device in response['response']:
            uptime = "N/A" if device['upTime'] is None else device['upTime']

            # this is for the case of switch stacks.. multiple serial and model numbers
            if  device['serialNumber'] is not None and "," in device['serialNumber']:
                serialPlatformList = zip(device['serialNumber'].split(","), device['platformId'].split(","))
            else:
                serialPlatformList = [(device['serialNumber'], device['platformId'])]
            for (serialNumber,platformId) in serialPlatformList:
                print("{0:42}{1:17}{2:12}{3:18}{4:12}{5:16}{6:15}".
                  format(device['hostname'],
                         device['managementIpAddress'],
                         serialNumber,
                         platformId,
                         device['softwareVersion'],
                         device['role'],uptime))

