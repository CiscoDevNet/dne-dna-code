#!/usr/bin/env python
from __future__ import print_function
from dnac_utils import dnac_token, create_url
import requests
import json

def deploy():
    headers = {'x-auth-token': token, 'content-type': 'application/json'}

    # create a url for this API call
    url = create_url('/v1/template-programmer/template/deploy')

    body = {
        "templateId": "d1b4c4b4-31b9-4419-b7ed-a5ce2bf7eb83",
        "targetInfo": [
            {
                "id": "10.10.22.70",
                "type": "MANAGED_DEVICE_IP",
                "params": {"description": "changed by DNA Center", "interface": "TenGigabitEthernet1/1/1"}
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
    print("deploymentID -->", deploymentId)

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


