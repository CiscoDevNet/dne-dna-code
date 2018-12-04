#!flask/bin/python

"""
Cisco CMX Notification Receiver

A simple example demonstrating how to interact with the CMX API.

Default port: 5004

Cisco CMX Documentation
https://www.cisco.com/c/en/us/td/docs/wireless/mse/10-2/api/b_cmx_102_api_reference.html
See also:
https://documentation.meraki.com/MR/Monitoring_and_Reporting/CMX_Analytics#CMX_Location_API

Written by: Matthew DeNapoli

"""

# Libraries
from pprint import pprint
from flask import Flask
from flask import json
from flask import request
from flask import render_template
from flask import Response
from queue import Queue
import sys, getopt
import json
import requests
import shutil
import atexit
import os
import time

mapImages = []

requests.packages.urllib3.disable_warnings()
app = Flask(__name__)
queue = Queue()

@app.route('/go', methods=['GET'])
def get_go():
    global mapImages
    global locationdata

    return render_template('index.html', mapImages = mapImages, \
    clientsraw = locationdata.text)


@app.route("/notification_stream")
def notification_handler_stream():
    def notification_stream():
        while True:
            the_notification = queue.get(True)
            print("Sending {}".format(the_notification))
            yield "data: " + the_notification + "\n\n"

    return Response(notification_stream(), mimetype="text/event-stream")

@app.route("/notification_handler", methods=['POST'])
def notification_handler():
    queue.put(json.dumps(request.get_json(force=True)))
    return "OK"

def create_notification(msg):
    global url
    global initials
    global username
    global password

    endpoint = "https://" + url + "/api/config/v1/notification"

    payload = \
    {
        "name": initials + "LocationUpdate",
        "userId": "learning",
        "rules": [
            {
                "conditions": []
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

    headers = {"Content-Type": "application/json"}

    print(json.dumps(payload))
    print(headers)

    response = requests.request("PUT", endpoint, \
    data=json.dumps(payload), headers=headers, auth=(username, password), verify=False)

    print(response.text)

def get_maps():
    global url
    global username
    global password
    global mapImages

    endpoint = "https://" + url + "/api/config/v1/maps"
    print("trying " + endpoint)

    try:
        mapdata = requests.request("GET", endpoint, auth=(username, password), verify=False)
        print("got maps")
        mapdatajson = json.loads(mapdata.text)
    except Exception as e:
        print(e)

    #Extract the hierarchy, image information, and actual image
    for campus in mapdatajson["campuses"]:
        for building in campus["buildingList"]:
            for floor in building["floorList"]:
                mapImages.append(
                    {
                        "hierarchy" : campus["name"] + ">" + \
                        building["name"] + ">" + \
                        floor["name"],
                        "imageName" : floor["image"]["imageName"],
                        "gpsMarkers" : floor["gpsMarkers"]
                    }
                )

                #Get actual image file and save locally
                endpoint = "https://" + url + \
                "/api/config/v1/maps/imagesource/" + \
                floor["image"]["imageName"]

                print("trying " + endpoint)

                try:
                    response = requests.request("GET", endpoint, \
                    auth=(username, password), stream=True, verify=False)
                    print("Got Map")

                    with open("static/" + \
                    floor["image"]["imageName"], 'wb') as f:
                        response.raw.decode_content = True
                        shutil.copyfileobj(response.raw, f)

                except Exception as e:
                    print(e)


def initialize_client_locations():
    global url
    global username
    global password
    global locationdata
    #Get the client location data
    endpoint = "https://" + url + "/api/location/v3/clients"
    print("trying " + endpoint)


    try:
        locationdata = requests.request("GET", endpoint, \
        auth=(username, password), verify=False)
        print("got data")
    except Exception as e:
        print(e)


#defining function to run on shutdown
def delete_notification():
    global url
    global username
    global password
    global initials

    endpoint = "https://" + url + "/api/config/v1/notifications/" + \
    initials + "LocationUpdate"
    try:
        requests.request("DELETE", endpoint, auth=(username, password), \
        verify=False)
    except Exception as e:
        print(e)

atexit.register(delete_notification)
# Launch application with supplied arguments

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
     "http://127.0.0.1:4040/api/tunnels", \
     verify=False)

    tunnels = json.loads(tunnels.text)
    tunnels = tunnels["tunnels"]

    for tunnel in tunnels:
        if tunnel['proto'] == 'http':
            msg = tunnel['public_url']

    print(msg)
    get_maps()
    initialize_client_locations()
    create_notification(msg)
    app.run(host="0.0.0.0", port=5004,threaded=True,debug=False)
