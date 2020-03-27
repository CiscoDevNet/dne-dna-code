#!/usr/bin/env python
from __future__ import print_function
from dnac_utils import dnac_token, create_url
import requests
import json


# Entry point for program.
if __name__ == '__main__':

    # get an authentication token.  The username and password is obtained from an environment file
    token = dnac_token()
    headers = {'x-auth-token' : token}

    # create a url for this API call
    url =  create_url('/v1/template-programmer/project')

    # make the REST request
    response = requests.get(url, headers=headers, verify=False)
    response.raise_for_status()

    # now print the templates
    for project in response.json():
        if project['templates']:
            print('Project:{}'.format(project['name']))
            for template in project['templates']:
                print ('\t{}:{}'.format(template['name'], template['id']))

