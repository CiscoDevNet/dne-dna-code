#!/usr/bin/env python
from __future__ import print_function
from dnac_utils import dnac_token, create_url, wait_on_task
import requests
import json
import sys
import ast

def post_and_wait(token, url, data):
    '''
    POST call, but waits for the task to complete.
    :param token: obtained earlier via authentication to dnac
    :param url: of the REST API
    :param data: the payload being sent
    :return: the task body
    '''
    headers= { 'x-auth-token': token, 'content-type' : 'application/json'}

    try:
        response = requests.post(url, headers=headers, data=json.dumps(data), verify=False)
    except requests.exceptions.RequestException  as cerror:
        print ("Error processing request", cerror)
        sys.exit(1)

    taskid = response.json()['response']['taskId']
    print ("Waiting for Task %s" % taskid)
    task_result = wait_on_task(taskid, token, timeout=25, retry_interval=5)

    return task_result

def execute_commands(token, deviceIdList, commandList):
    '''
    runs the list of commands on the list of devices
    :param token: obtained earlier via authentication to dnac
    :param deviceIdList:  a list of device UUID to run the commands on
    :param commandList: a list of IOS commands (exec-only, no config) to run on the deviceList
    :return: a fileId containing the output of the commands
    '''
    url = create_url('/v1/network-device-poller/cli/read-request')
    headers = {'x-auth-token' : token,
               'content-type' : 'application/json'}
    payload ={
        "name" : "my commands",
        "commands" : commandList,
        "deviceUuids" : deviceIdList
        }
    task_result = post_and_wait(token,url, payload)
    print ("task complete")

    # the value of "progress" is a string, but needs to be interprettd as json.
    return ast.literal_eval(task_result['progress'])['fileId']


def get_deviceIdList(token, *deviceIps):
    '''
    converts a list of device IP adddreses into device UUID
    :param token: obtained earlier via authentication to dnac
    :param deviceIps: a list of deviceIps
    :return: a list of UUID
    '''
    headers = {'x-auth-token': token}
    deviceIdList =[]
    for deviceIp in deviceIps:
        url = create_url("/v1/network-device/ip-address/{}".format(deviceIp))
        response = requests.get(url, headers=headers, verify=False)
        response.raise_for_status()
        deviceIdList.append(response.json()['response']['id'])

    return deviceIdList

def download_results(token, results_fileId):
    '''
    obtains the result file by it's UUID from DNAC
    :param token: obtained earlier via authentication to dnac
    :param results_fileId: the fileId of the results file
    :return: the contents of the file as json. NOTE: This is really text, but gets converted to json by requests
    '''
    headers = {'x-auth-token': token}
    url = create_url('/v1/file/{}'.format(results_fileId))

    response = requests.get(url, headers=headers, verify=False)
    return response.json()

def format_results(results):
    '''
    pretty prints the results
    :param results:
    :return:
    '''
    print()
    print("Results:")
    for result in results:
        devId = result['deviceUuid']
        commands = result['commandResponses']['SUCCESS'].keys()
        for cmd in commands:
            display = ','.join(result['commandResponses']['SUCCESS'][cmd].split('\n'))
            print ('DevId,{},{}'.format(devId, display))

# Entry point for program.
if __name__ == '__main__':

    # get an authentication token.  The username and password is obtained from an environment file
    token = dnac_token()

    # look up the device ID
    deviceIdList = get_deviceIdList(token,"10.10.22.70")

    # a list of commands to run - in this case just two
    commandList = ["show ver | inc Software, Version", "show clock"]

    # now run the commands
    results_fileId = execute_commands(token, deviceIdList, commandList)

    # we get back a fileId with the results. NOTE: technically this is a textfile, but requests will redner in JSON
    results = download_results(token, results_fileId)

    # now print them out in a nice format
    format_results(results)
