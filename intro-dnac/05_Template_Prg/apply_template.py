#!/usr/bin/env python
from __future__ import print_function
from dnac_utils import dnac_token, create_url
import requests
import json
import time

def deploy():
    headers = {'x-auth-token': token, 'content-type': 'application/json'}

    # create a url for this API call
    url = create_url('/v1/template-programmer/template/deploy')

    body = {
        "templateId": "af2c57dc-769f-47af-9f36-96a12746286a",
        "targetInfo": [
            {
                "id": "10.10.20.82",
                "type": "MANAGED_DEVICE_IP",
                "params": {"description": "changed by DNA Center {}".format(time.time()), "interface": "TenGigabitEthernet1/1/1"}
            }
        ]
    }

    # make the REST request
    response = requests.post(url, headers=headers, data=json.dumps(body), verify=False)
    response.raise_for_status()
    deploymentId = response.json()['deploymentId']

    # clean response to grab DeploymentID
    deploymentId = deploymentId.split(':')
    deploymentId = deploymentId[-1]
    deploymentId = deploymentId.replace(" ", "")
    print("deploymentID -->", deploymentId)
    time.sleep(5)

    # now look for the status
    url = create_url('/v1/template-programmer/template/deploy/status/{}'.format(deploymentId))
    response = requests.get(url, headers=headers, verify=False)
    response.raise_for_status()
    print(json.dumps(response.json(), indent=2))


# Entry point for program.
if __name__ == '__main__':

    # get an authentication token.  The username and password is obtained from an environment file
    token = dnac_token()
    deploy()


