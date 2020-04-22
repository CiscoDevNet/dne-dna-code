import requests
import os
import json
from requests.auth import HTTPBasicAuth  # for Basic Auth
import sys
import time
# Get the absolute path for the directory where this file is located "here"
here = os.path.abspath(os.path.dirname(__file__))

# Get the absolute path for the project / repository root
project_root = os.path.abspath(os.path.join(here, "../.."))

# Extend the system path to include the project root and import the env files
sys.path.insert(0, project_root)

import env_lab


DNAC_URL = env_lab.DNA_CENTER["host"]
DNAC_USER = env_lab.DNA_CENTER["username"]
DNAC_PASS = env_lab.DNA_CENTER["password"]


ios_cmd = "" # TODO 1 Enter the IOS command for command runner API here!


# TODO 2 Building your Authentication function below.
#        Complete the API request below.
#        Stuck? look back at 01_Authentication code sample
def get_auth_token():
    global token
    url =                           #TODO
    hdr =                           #TODO
    resp =                          #TODO
    token = resp.json()['Token']
    print(" Cisco DNA Center Token Retrieved: {}".format(token))


# TODO 3 Construct the function below to get a list of all devices from DNAC
#        Complete the API request below.
#        Stuck? look back at 02_Network_Devices code sample
def get_device_list():
    url =                           #TODO
    hdr =                           #TODO
    resp =                          #TODO
    device_list = resp.json()['response']
    filtered_device_list = []
    for device in device_list:
        if device['family'] == 'Switches and Hubs' or device['family'] == 'Routers':
            device_info = {}
            device_info['id'] = device['id']
            device_info['reachabilityStatus'] = device['reachabilityStatus']
            device_info['serialNumber'] = device['serialNumber']
            device_info['family'] = device['family']
            device_info['hostname'] = device['hostname']
            device_info['macAddress'] = device['macAddress']
            filtered_device_list.append(device_info)
    return filtered_device_list


# TODO 4 The function below initiates command runner request
#        Complete the API request below.
#        Stuck? look back at 04_Cmd_Runner code sample
def initiate_cmd_runner(device_id):
    param =                           #TODO
    url =                             #TODO
    header =                          #TODO
    response =                        #TODO
    task_id = response.json()['response']['taskId']
    print("Command runner Initiated! for device {}. Here's the TaskID {}".format(device['hostname'], task_id))
    return {"task_id": task_id, "hostname": device['hostname'], "family": device['family']}


# TODO 5 The function below checks the status of the preview request if it was done
#        Complete the API request below.
#        Hint: Function param `task` is of type dictionary, use task['task_id'] to access the taskId to be passed to the API call
#        Stuck? look back at 04_Cmd_Runner code sample
def get_task_info(task):
    url =                           #TODO
    hdr =                           #TODO
    task_result =                   #TODO
    file_id = task_result.json()['response']['progress']
    if "fileId" in file_id:
        unwanted_chars = '{"}'
        for char in unwanted_chars:
            file_id = file_id.replace(char, '')
        file_id = file_id.split(':')
        file_id = file_id[1]
        print("Task completed! Here's the FileID {}".format(file_id))
    else:  # recursive call to this function as the Task is not complete yet. keep checking
        get_task_info(task['task_id'])
        return task
    task['file_id'] = file_id
    print("Task completed! Here's the FileID {} for command ran on {}".format(task['file_id'], task['hostname']))
    return task


# TODO 6 The function below checks the status of the preview request if it was done
#        Complete the API request below.
#        Hint: Function param `file` is of type dictionary, use file['file_id'] to access the fileID to be passed to the API call
#        Stuck? look back at 04_Cmd_Runner code sample
def get_cmd_output(file):
    url =                           #TODO
    hdr =                           #TODO
    cmd_result =                    #TODO
    command_responses = cmd_result.json()[0]['commandResponses']
    if command_responses['SUCCESS']:
        command_output = command_responses['SUCCESS'][ios_cmd]
    elif command_responses['FAILURE']:
        command_output = command_responses['FAILURE'][ios_cmd]
    else:
        command_output = command_responses['BLACKLISTED'][ios_cmd]
    file['cmd_out'] = command_output
    return file

# TODO 7 Nothing to be changed here.
#  This function creates the repo for the command output and stores them in an organized fashion.
#  Inspect the code
def save_config(output):
    global filename, path_to_file
    filename = str(output['hostname']) + '_run_config.txt'
    path_to_file = "./device_config/" + str(output['family'] + "/" + str(output['hostname']))
    if not os.path.exists(path_to_file):
        os.makedirs(path_to_file)
    with open(os.path.join(path_to_file, filename), 'w') as f_temp:
        f_temp.write(output['cmd_out'])
        f_temp.seek(0)  # reset the file pointer to 0
        f_temp.close()
    print("Running config on device {} was saved to {}".format(file['hostname'], path_to_file))


# TODO [Bonus] you've completed all your TODOs already? does the code run? :)
#   have extra time?
#   incorporate version control (git) within this script to have a configuration version control for your devices

if __name__ == '__main__':
    task_id_list = []
    file_id_list = []
    command_output = []
    get_auth_token()
    device_list = get_device_list()
    # print("Device List: ", device_list)
    for device in device_list:
        task_id_list.append(initiate_cmd_runner(device['id']))
    # print("Task List: ", task_id_list)
    for task in task_id_list:
        file_id_list.append(get_task_info(task))
    # print("File List: ", file_id_list)
    for file in file_id_list:
        command_output = get_cmd_output(file)
        save_config(command_output)