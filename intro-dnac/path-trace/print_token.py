#! /usr/bin/env python
from env_lab import apicem
import requests
import json
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

    # print the token
    print(response.text)
