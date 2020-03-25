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

THE SOFTWARE IS PROVIDED 'AS IS', WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

# Libraries
from pprint import pprint
from flask import Flask, json, request, render_template
import sys, os, getopt, json
from webexteamssdk import WebexTeamsAPI
import requests

# Get the absolute path for the directory where this file is located "here"
here = os.path.abspath(os.path.dirname(__file__))

# Get the absolute path for the project / repository root
project_root = os.path.abspath(os.path.join(here, ".."))

# Extend the system path to include the project root and import the env files
sys.path.insert(0, project_root)
import env_user  # noqa

# WEBEX TEAMS LIBRARY
teamsapi = WebexTeamsAPI(access_token=env_user.WT_ACCESS_TOKEN)

# Flask App
app = Flask(__name__)

# Webhook Receiver Code - Accepts JSON POST from Meraki and 
# Posts to WebEx Teams
@app.route("/", methods=["POST"])
def get_webhook_json():
    global webhook_data

    # Webhook Receiver
    webhook_data = request.json
    pprint(webhook_data, indent=1)
    webhook_data = json.dumps(webhook_data)
    # WebEx Teams can only handle so much text so limit to 1000 chars
    webhook_data = webhook_data[:1000] + '...'

    # Send Message to WebEx Teams
    teamsapi.messages.create(
        env_user.WT_ROOM_ID,
        text="Meraki Webhook Alert: " + webhook_data
    )

    # Return success message
    return "WebHook POST Received"

# Launch application with supplied arguments
def main(argv):
    try:
        opts, args = getopt.getopt(argv, "hs:", ["secret="])
    except getopt.GetoptError:
        print("webhookreceiver.py -s <secret>")
        sys.exit(2)
    for opt, arg in opts:
        if opt == "-h":
            print("webhookreceiver.py -s <secret>")
            sys.exit()
        elif opt in ("-s", "--secret"):
            secret = arg

    print("secret: " + secret)


if __name__ == "__main__":
    main(sys.argv[1:])
    app.run(host="0.0.0.0", port=5005, debug=False)
