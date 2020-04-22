import requests
import os
import json
from requests.auth import HTTPBasicAuth  # for Basic Auth
import env_lab
import time

DNAC_URL = env_lab.DNA_CENTER["host"]
DNAC_USER = env_lab.DNA_CENTER["username"]
DNAC_PASS = env_lab.DNA_CENTER["password"]


ios_cmd = "show run"


def get_auth_token():
    global token                                                                          # Setting Token global var
    url = 'https://{}/dna/system/api/v1/auth/token'.format(DNAC_URL)                      # Endpoint URL
    hdr = {'content-type' : 'application/json'}                                           # Define request header
    resp = requests.post(url, auth=HTTPBasicAuth(DNAC_USER, DNAC_PASS), headers=hdr)      # Make the POST Request
    token = resp.json()['Token']                                                          # Retrieve the Token
    print("Token Retrieved: {}".format(token))                                            # Print out the Token


def get_device_list():
    """
    Building out function to retrieve list of devices. Using requests.get to make a call to the network device Endpoint
    """
    url = "https://{}/api/v1/network-device".format(DNAC_URL)
    hdr = {'x-auth-token': token, 'content-type' : 'application/json'}
    resp = requests.get(url, headers=hdr)  # Make the Get Request
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


def initiate_cmd_runner(device_id):
        param = {
            "name": "Show Command",
            "commands": [ios_cmd],
            "deviceUuids": [device_id]
        }
        url = "https://{}/dna/intent/api/v1/network-device-poller/cli/read-request".format(DNAC_URL)
        header = {'content-type': 'application/json', 'x-auth-token': token}
        response = requests.post(url, data=json.dumps(param), headers=header)
        task_id = response.json()['response']['taskId']
        print("Command runner Initiated! for device {}. Here's the TaskID {}".format(device['hostname'], task_id))
        return {"task_id": task_id, "hostname": device['hostname'], "family": device['family']}


def get_task_info(task):
    url = "https://{}/dna/intent/api/v1/task/{}".format(DNAC_URL, task['task_id'])
    hdr = {'x-auth-token': token, 'content-type' : 'application/json'}
    task_result = requests.get(url, headers=hdr)
    file_id = task_result.json()['response']['progress']
    #time.sleep(6)
    if "fileId" in file_id:
        unwanted_chars = '{"}'
        for char in unwanted_chars:
            file_id = file_id.replace(char, '')
        file_id = file_id.split(':')
        file_id = file_id[1]
    else: # recursive call to this function as the Task is not completed yet
        get_task_info(task)
        return task
    task['file_id'] = file_id
    print("Task completed! Here's the FileID {} for command ran on {}".format(task['file_id'], task['hostname']))
    return task


def get_cmd_output(file):
    url = "https://{}/dna/intent/api/v1/file/{}".format(DNAC_URL, file['file_id'])
    hdr = {'x-auth-token': token, 'content-type': 'application/json'}
    cmd_result = requests.get(url, headers=hdr, stream=True)
    command_responses = cmd_result.json()[0]['commandResponses']
    if command_responses['SUCCESS']:
        command_output = command_responses['SUCCESS'][ios_cmd]
    elif command_responses['FAILURE']:
        command_output = command_responses['FAILURE'][ios_cmd]
    else:
        command_output = command_responses['BLACKLISTED'][ios_cmd]
    file['cmd_out'] = command_output
    return file


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