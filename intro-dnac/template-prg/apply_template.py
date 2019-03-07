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
        "templateId": "967c8430-96cd-4445-8fc4-72543b624d9f",
        "targetInfo": [
            {
                "id": "10.10.22.70",
                "type": "MANAGED_DEVICE_IP",
                "params": {"description": "changed by DNAC", "interface": "TenGigabitEthernet1/0/24"}
            }
        ]
    }

    # make the REST request
    response = requests.post(url, headers=headers, data=json.dumps(body), verify=False)
    response.raise_for_status()
    deploymentId = response.json()['deploymentId']

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


