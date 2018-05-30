#!/usr/bin/env python
from __future__ import print_function
from dnac_utils import dnac_token, create_url
import requests
import time
import json


# Entry point for program.
if __name__ == '__main__':

    # get an authentication token.  The username and password is obtained from an environment file
    token = dnac_token()
    headers = {'x-auth-token' : token}

    # create a url for this API call
    url =  create_url('/v1/template-programmer/template/version/{}'.format('3f7c91b4-4b17-4545-af58-290d51f1de55'))

    # make the REST request
    response = requests.get(url, headers=headers, verify=False)
    response.raise_for_status()

    template = response.json()[0]
    #build a dict with version as key
    print('Project:{} Template:{}'.format(template['projectName'], template['name']))

    versions = {}
    for version in template['versionsInfo']:
        if 'version' in version:
            versions[version['version']] = '{} {} {}'.format(version['id'],
                                                             time.strftime('%Y-%m-%d:%H:%M:%S',
                                                                           time.localtime(version['versionTime']/1000)),
                                                             version['versionComment'])
    print("  Ver|{:37}{:20} Comment".format('  templateId for version of template',
                                         'Time of commit'))
    for v in sorted(versions.keys()):
        print('  {:3}|{}'.format(v, versions[v]))

    latest_version = sorted(versions.keys())[-1]
    latest_versionId = versions[latest_version].split()[0]
    print()
    print ("Getting template for latest version:{}".format(latest_versionId))

    url = create_url('/v1/template-programmer/template/{}'.format(latest_versionId))
    response = requests.get(url, headers=headers, verify=False)
    response.raise_for_status()

    print(json.dumps(response.json(),indent=2))
