"""The provided sample code in this repository will reference this file to get the
information needed to connect to your lab backend.  You provide this info here
once and the scripts in this repository will access it as needed by the lab.
Copyright (c) 2019 Cisco and/or its affiliates.
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

# Libraries
from pprint import pprint
import sys, os, getopt, json, time, datetime
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

# MERAKI BASE URL 
base_url = "https://api.meraki.com/api/v0"

def getnetworklist():
    orgs = ""

    # Get Orgs that entered Meraki API Key has access to
    try:
        # MISSION TODO
        orgs = requests.get(
            base_url + "TODO:ADD URL TO GET ORGANIZATION LIST HERE",
            headers={
                "X-Cisco-Meraki-API-Key": env_user.MERAKI_API_KEY,
            }
        )
        # Deserialize response text (str) to Python Dictionary object so
        # we can work with it
        orgs = json.loads(orgs.text)
        pprint(orgs)
        # END MISSION SECTION
    except Exception as e:
        pprint(e)

    # Now get a specific network based on name added on command line
    networks = ""
    if orgs != "":
        for org in orgs:
            try:
                # MISSION TODO
                networks = requests.get(
                    base_url + "TODO:ADD URL TO GET NETWORK LIST HERE (be sure to add organization id to the string)",
                    headers={
                        "X-Cisco-Meraki-API-Key": env_user.MERAKI_API_KEY,
                    })
                # Deserialize response text (str) to Python Dictionary object so
                # we can work with it
                networks = json.loads(networks.text)
                pprint(networks)
                return networks
                # END MISSION SECTION
            except Exception as e:
                pprint(e)
                return ""
    
    return "No Networks Found"


def get_mx_l3_firewall_rules(network):
    # return the MX L3 firewall ruleset for a network
    try:
        # MISSION TODO
        rules = requests.get(
                base_url + "TODO:ADD URL TO GET L3 Firewall Rules HERE (be sure to add network id to the string)",
                headers={
                    "X-Cisco-Meraki-API-Key": env_user.MERAKI_API_KEY,
                })
        pprint(network + ": " + rules.text)
        return rules.text
        # END MISSION SECTION
    except Exception as e:
        pprint("Rules lookup failed")
        pprint(e)
        return ""

def createbackup(networks):
    # create directory to place backups
    flag_creationfailed = True
    MAX_FOLDER_CREATE_TRIES = 5
    for i in range(0, MAX_FOLDER_CREATE_TRIES):
        time.sleep(2)
        timestamp = "{:%Y%m%d_%H%M%S}".format(datetime.datetime.now())
        directory = "mxfwctl_backup_" + timestamp
        flag_noerrors = True
        try:
            os.makedirs(directory)
        except Exception as e:
            print(e)
            flag_noerrors = False
        if flag_noerrors:
            flag_creationfailed = False
            break

    if flag_creationfailed:
        pprint("Unable to create directory for backups")
        sys.exit(2)
    else:
        pprint('INFO: Backup directory is ' + directory)

    # create backups - one file per network
    for network in networks:
        rules = get_mx_l3_firewall_rules(network["id"])
        if rules != "":
            filename = network["id"] + ".json"
            filepath = directory + "/" + filename
            if os.path.exists(filepath):
                pprint(
                    "Cannot create backup file: name conflict " + filename
                )
                sys.exit(2)
            else:
                try:
                    f = open(filepath, "w")
                except Exception as e:
                    pprint(
                        "Unable to open file path for writing: " + filepath
                    )
                    sys.exit(2)


                f.write(rules)

                try:
                    f.close()
                except Exception as e:
                    pprintusertext(
                        "Unable to close file path: " + filepath
                    )
                    sys.exit(2)

                pprint(
                    "INFO: Created backup for " + network["name"]
                )

                teamsapi.messages.create(
                    env_user.WT_ROOM_ID,
                    files=[filepath],
                    text="Network " + network["name"] + " L3 Rules Backup",
                )
        else:
            pprint(
                "WARNING: Unable to read MX ruleset for " + network["name"]
            )
            
    return (0)    

# Launch application
if __name__ == "__main__":
    # Configuration parameters
    networks = getnetworklist()
    createbackup(networks)
