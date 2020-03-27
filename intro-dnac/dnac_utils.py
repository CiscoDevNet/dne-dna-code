#!/usr/bin/env python
"""This is a sample script for a DNA Center Programmability Learning Lab.

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


# Get the absolute path for the directory where this file is located "here"
here = os.path.abspath(os.path.dirname(__file__))

# Get the absolute path for the project / repository root
project_root = os.path.abspath(os.path.join(here, "../.."))


# Extend the system path to include the project root and import the env files
#sys.path.insert(0, project_root)

import env_lab
from time import sleep, time
import requests
import sys
import urllib3
from requests.auth import HTTPBasicAuth
RETRY_INTERVAL=5
# Silence the insecure warning due to SSL Certificate
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
# -------------------------------------------------------------------
# Custom exception definitions
# -------------------------------------------------------------------
class TaskTimeoutError(Exception):
    pass

class TaskError(Exception):
    pass

DNAC_URL = env_lab.DNA_CENTER["host"]
DNAC_USER = env_lab.DNA_CENTER["username"]
DNAC_PASS = env_lab.DNA_CENTER["password"]


def dnac_token(host=DNAC_URL,
                username=DNAC_USER,
                password=DNAC_PASS):
    """
    Use the REST API to Log into an DNA_CENTER and retrieve token
    """
    url = "https://{}/api/system/v1/auth/token".format(host)
    # Make Login request and return the response body
    response = requests.request("POST", url, auth=HTTPBasicAuth(username, password), verify=False)

    return response.json()["Token"]


def create_url(url, host=DNAC_URL):
    return "https://{}/api{}".format(host,url)


def wait_on_task(deployment_id, token, timeout=(5 * RETRY_INTERVAL), retry_interval=RETRY_INTERVAL):
    """ Waits for the specified task to complete
    """

    task_url = create_url("/v1/task/{}".format(deployment_id))

    headers = {
        "x-auth-token": token
    }
    start_time = time()

    while True:
        result = requests.get(url=task_url, headers=headers, verify=False)
        result.raise_for_status()

        response = result.json()["response"]

        if "endTime" in response:
            return response
        else:
            if timeout and (start_time + timeout < time()):
                raise TaskTimeoutError("Task %s did not complete within the specified timeout "
                                       "(%s seconds)" % (deployment_id, timeout))

            print("Task=%s has not completed yet. Sleeping %s seconds..." % (deployment_id, retry_interval))
            sleep(retry_interval)

        if response['isError'] == True:
            raise TaskError("Task %s had error %s" % (deployment_id, response['progress']))

    return response