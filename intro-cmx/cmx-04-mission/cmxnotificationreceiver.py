"""Set the Environment Information Needed to Access Your Lab!

The provided sample code in this repository will reference this file to get the
information needed to connect to your lab backend.  You provide this info here
once and the scripts in this repository will access it as needed by the lab.


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


import sys
import getopt
import requests
import time
import datetime
import os
import re
import ciscosparkapi
from pprint import pprint
from flask import Flask
from flask import json
from flask import request
from flask import render_template
from flask import Response

# Get the absolute path for the directory where this file is located "here"
here = os.path.abspath(os.path.dirname(__file__))

# Get the absolute path for the project / repository root
project_root = os.path.abspath(os.path.join(here, "../.."))

# Extend the system path to include the project root and import the env files
sys.path.insert(0, project_root)
import env_lab  # noqa
import env_user  # noqa


# Create a Cisco Spark object
spark = ciscosparkapi.CiscoSparkAPI(access_token=env_user.SPARK_ACCESS_TOKEN)

requests.packages.urllib3.disable_warnings()
app = Flask(__name__)

def create_notification(msg):
    global url
    global initials
    global username
    global password

    # MISSION TODO
    endpoint = "https://" + url + "CMX API ENDPOINT TO CREATE NOTIFICATIONS"

    payload = \
    {
        "name": initials + "LocationUpdate",
        "userId": "learning",
        "rules": [
            {
                "conditions":[
                    {
                        "condition": "locationupdate.macAddressList == MAC ADDRESS TO BE FOUND;"
                    }
                ]
            }
        ],
        "subscribers": [
            {
                "receivers": [
                    {
                        "uri": msg + ":80" + \
                        "/notification_handler",
                        "messageFormat": "JSON",
                        "headers": None,
                        "qos": "AT_MOST_ONCE"
                    }
                ]
            }
        ],
        "enabled": True,
        "internal": False,
        "cloud": True,
        "enableMacScrambling": False,
        "macScramblingSalt": "learning",
        "notificationType": "LocationUpdate"
    }
    # END MISSION TODO
    headers = {"Content-Type": "application/json"}

    print(json.dumps(payload))
    print(headers)

    response = requests.request("PUT", endpoint, \
    data=json.dumps(payload), headers=headers, auth=(username, password), verify=False)

    print(response.text)


@app.route("/notification_handler", methods=['POST'])
def notification_handler():
    r_json = request.get_json(force=True)
    deviceId = r_json["notifications"][0]["deviceId"]
    location = r_json["notifications"][0]["locationMapHierarchy"]
    spark.messages.create(
        env_user.SPARK_ROOM_ID,
        text="CMX Mission Accomplished!  Device " \
        + deviceId + " found at location: " + location,
    )

    delete_notification()
    return "done"


def delete_notification():
    global url
    global username
    global password
    global initials

    # MISSION TODO
    endpoint = "https://" + url + "CMX API ENDPOINT TO DELETE NOTIFICATIONS" + \
    initials + "LocationUpdate"
    # END MISSION TODO
    try:
        requests.request("DELETE", endpoint, auth=(username, password), \
        verify=False)
    except Exception as e:
        print(e)

def main(argv):
    global url
    global initials
    global username
    global password


    try:
       opts, args = getopt.getopt(argv,"hu:p:l:i:",["username=","password=",\
       "url=","initials="])
    except getopt.GetoptError:
       print ('cmxnotificationreceiver.py -u <username> -p \ <password> -l <url> -i <initials>')
       sys.exit(2)
    for opt, arg in opts:
       if opt == '-h':
           print ('cmxnotificationreceiver.py -u <username> -p <password> \
            -l <url> -i <initials>')
           sys.exit()
       elif opt in ("-u", "--username"):
           username  = arg
       elif opt in ("-p", "--password"):
           password = arg
       elif opt in ("-l", "--url"):
           url = arg
       elif opt in ("-i", "--initials"):
           initials = arg

    print ('username: '+ username)
    print ('password: '+ password)
    print ('url: '+ url)
    print ('initials: ' + initials)

if __name__ == '__main__':
    main(sys.argv[1:])
    time.sleep(10)

    tunnels = requests.request("GET", \
     "http://ngrok:4040/api/tunnels", \
     verify=False)

    tunnels = json.loads(tunnels.text)
    tunnels = tunnels["tunnels"]

    for tunnel in tunnels:
        if tunnel['proto'] == 'http':
            msg = tunnel['public_url']

    print(msg)
    create_notification(msg)
    app.run(host="0.0.0.0", port=5004,threaded=True,debug=False)
