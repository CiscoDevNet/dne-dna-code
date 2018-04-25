#!/usr/bin/env python
"""DNAv3 - NFVIS mission

In this mission we follow the following steps to build our code:

1.Destroy any existing VNFs on NFVIS
2.Verify images exist on NFVIS
3.Create service network on NFVIS
4.Instantiate ISRv and ASAv
5.Verify VNFs are running
6.Create alert in Spark Room

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
import requests
import json
import os
import sys
import nfvis_payload
import time
import ciscosparkapi

# Get the absolute path for the directory where this file is located "here"
here = os.path.abspath(os.path.dirname(__file__))

# Get the absolute path for the project / repository root
project_root = os.path.abspath(os.path.join(here, "../.."))


# Extend the system path to include the project root and import the env files
sys.path.insert(0, project_root)

import env_lab
import env_user

NFVIS_USERNAME = env_lab.NFVIS_SERVER['username']
NFVIS_PASSWORD = env_lab.NFVIS_SERVER['password']
NFVIS = env_lab.NFVIS_SERVER['host']
new_bridge = "svc-br"
new_network = "svc-net"

requests.packages.urllib3.disable_warnings()

spark = ciscosparkapi.CiscoSparkAPI(access_token=env_user.SPARK_ACCESS_TOKEN)

def nvfis_getgcred():
    login = NFVIS_USERNAME
    password = NFVIS_PASSWORD
    url = "https://" + NFVIS
    nip = NFVIS
    return nip, url, login, password

# MISSION TODO 1: Provide the NFVIS REST API endpoint needed
# to get the detailed running images configuration

def nfv_get_image_configuration(s, url):
    u = url + '/MISSION'
    image_configurations = s.get(u)
    r_image_configuration = json.loads(image_configurations.content)

    return r_image_configuration

# END MISSION SECTION

# MISSION TODO 2: Provide the header for content data

def nfv_verify_device_deployment(s, url):
    s.headers = ({'MISSION': 'application/vnd.yang.data+json',
                      'Accept': 'application/vnd.yang.collection+json'})
    u = url + '/api/operational/vm_lifecycle/opdata/tenants/tenant/admin/deployments/'
    nfv_deployment_page = s.get(u)

    if nfv_deployment_page.status_code != 200:
        # Set headers back to default
        s.headers = ({'MISSION': 'application/vnd.yang.data+json', 'Accept': 'application/vnd.yang.data+json'})
        return False
    else:
        r_nfv_deployment_page = json.loads(nfv_deployment_page.content)
        # Set headers back to default
        s.headers = ({'MISSION': 'application/vnd.yang.data+json', 'Accept': 'application/vnd.yang.data+json'})
        return r_nfv_deployment_page

# END MISSION SECTION

def nfv_get_count_of_vm_deployments(s, url):
    u = url + '/api/config/vm_lifecycle/tenants/tenant/admin/deployments'
    count_vm_deployed_page = s.get(u)
    r_count_vm_deployed_page = json.loads(count_vm_deployed_page.content)

    for iv in r_count_vm_deployed_page.values():
        vm_deployed_count = len(iv['deployment'])
        return vm_deployed_count

# MISSION TODO 3: Specify the payload to create a new bridge

def nfv_create_newbridge(s, url, new_bridge):
    u = url + "/api/config/bridges"
    make_bridge_payload = '{ "bridge": {"name": "%s" }}' % new_bridge
    r_create_bridge = s.post(u, data=MISSION)
    if '201' in r_create_bridge:
        return True
    else:
        return r_create_bridge

# END MISSION SECTION

def nfv_create_new_network(s, url, new_network, new_bridge):
    u = url + "/api/config/networks"
    createnet_payload = '{ "network": {"name": "%s" , "bridge": "%s" }}' % (new_network, new_bridge)
    r_create_net = s.post(u, data=createnet_payload)
    return r_create_net

# MISSION TODO 4: Specify the response code when a VM was successfully deployed

def nfv_deploy_vm(s, url, data):
    u = url + "/api/config/vm_lifecycle/tenants/tenant/admin/deployments"

    deployed_vm_page = s.post(u, data=data)
    r_deployed_vm_page = str(deployed_vm_page)
    if "MISSION" in r_deployed_vm_page:
        return True
    else:
        return False

# END MISSION SECTION

def nfv_delete_vm(s, url, data):
	u = url + "/api/config/vm_lifecycle/tenants/tenant/admin/deployments/deployment/" + data

	deleted_vm_page = s.delete(u)
	r_deleted_vm_page = str(deleted_vm_page)
	if "204" in r_deleted_vm_page:
		return True
	else:
		return False

if __name__ == '__main__':

    # basic credential setup for NFVIS device
    nip, url, login, password = nvfis_getgcred()
    s = requests.Session()
    s.auth = (login, password)
    s.headers = ({'Content-type': 'application/vnd.yang.data+json', 'Accept': 'application/vnd.yang.data+json'})
    s.verify = False
    print (nip, url, login, password)

    print ("STEP 1 - Verify device deployments and delete if there are any")
    r_vm_device_deployment = nfv_verify_device_deployment(s, url)
    if r_vm_device_deployment != False:
        for deployment in r_vm_device_deployment['collection']['vmlc:deployments']:
            delete_deployment = deployment['deployment_name']

            nfv_delete_vm(s, url, delete_deployment)
            time.sleep(10)

# MISSION TODO 5: Specify the correct parameter to parse and extract from the
# output below

    print ("STEP 2 - Verify images exist")
    images = nfv_get_image_configuration(s,url)
    for image in images['vmlc:images']['MISSION']:
        print (image['name'])

# END MISSION SECTION

    print ("STEP 3.1 - Create bridge")
    r_create_lanbridge = nfv_create_newbridge(s, url, new_bridge)

    print ("STEP 3.2 - Create network and associate with bridge")
    r_create_net = nfv_create_new_network(s, url, new_network, new_bridge)

    print ("STEP 4.1 - Start ISR")
    r_create_isr = nfv_deploy_vm(s, url, json.dumps(nfvis_payload.isr_payload))
    print (r_create_isr)

    print ("STEP 4.2 - Start ASA")
    r_create_asa = nfv_deploy_vm(s, url, json.dumps(nfvis_payload.asa_payload))
    print (r_create_asa)

    print ("STEP 5.1 - Count running VMs")
    r_vm_deployed_count = nfv_get_count_of_vm_deployments(s, url)
    print (r_vm_deployed_count)

    print ("STEP 5.2 - Verify device deployments")
    r_vm_device_deployment = nfv_verify_device_deployment(s, url)
    print (json.dumps(r_vm_device_deployment, indent=4, sort_keys=True))

    print ("STEP 6 - Send Spark message")
    message = spark.messages.create(env_user.SPARK_ROOM_ID,
            text='NFVIS mission completed')
    print (message)
