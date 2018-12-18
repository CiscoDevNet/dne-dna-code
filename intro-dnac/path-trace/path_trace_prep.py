#! /usr/bin/env python

from env_lab import apicem
from time import sleep
import json
import requests
import sys
import urllib3
from requests.auth import HTTPBasicAuth

# Silence the insecure warning due to SSL Certificate
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

headers = {
              'content-type': "application/json",
              'x-auth-token': ""
          }

def apic_login(host, username, password):
    """
    Use the REST API to Log into an DNA_CENTER and retrieve token
    """
    url = "https://{}/dna/system/api/v1/auth/token".format(host)

    # Make Login request and return the response body
    response = requests.request("POST", url, auth=HTTPBasicAuth(username, password),
                                headers=headers, verify=False)
    # print response
    return response.json()["Token"]


# Entry point for program
if __name__ == '__main__':
    # Setup Arg Parse for Command Line parameters
    import argparse
    parser = argparse.ArgumentParser()

    # Command Line Parameters for Source and Destination IP
    parser.add_argument("source_ip", help = "Source IP Address")
    parser.add_argument("destination_ip", help = "Destination IP Address")
    args = parser.parse_args()

    # Get Source and Destination IPs from Command Line
    source_ip = args.source_ip
    destination_ip = args.destination_ip

    # Print Starting message
    print("Running Troubleshooting Script for ")
    print("      Source IP:      {} ".format(source_ip))
    print("      Destination IP: {}".format(destination_ip))
    print("")

    # Log into the dna-EM Controller to get Ticket
    login = apic_login(apicem["host"], apicem["username"], apicem["password"])
