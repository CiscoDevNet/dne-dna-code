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


class c_organizationdata:

    def __init__(self):
        self.name = ""
        self.id = ""
        self.nwdata = []
        # List of dictionaries as returned by cloud. Primary key is 'id'

# end class


# Used for time.sleep(API_EXEC_DELAY). Delay added to avoid hitting dashboard
# API max request rate
API_EXEC_DELAY = 0.21


def printusertext(p_message):
    # prints a line of text that is meant for the user to read
    # do not process these lines when chaining scripts
    print("@ %s" % p_message)


def printhelp():
    # prints help text

    printusertext(
        "This is a script to manage firewall rulesets, by backing them up, \
        inserting new rules"
    )
    printusertext("or replacing the whole ruleset.")
    printusertext("")
    printusertext("To run the script, enter:")
    printusertext(
        "python mxfirewallcontrol.py -k <key> \
    [-c <command>]"
    )
    printusertext("")
    printusertext("Mandatory arguments:")
    printusertext("  -k <key>     : Your Meraki Dashboard API key")
    printusertext(
        "  -c create-backup  : Save rulesets in folder \
    mxfirewallctl_backup_<timestamp> as"
    )
    printusertext(' filenames "<org name>__<net name>.txt"')


def getorglist(p_apikey):
    # returns the organizations' list for a specified admin

    time.sleep(API_EXEC_DELAY)
    try:
        # MISSION TODO
        r = requests.get(
            "MISSION: REPLACE WITH ORGANIZATIONS API CALL",
            headers={
                "X-Cisco-Meraki-API-Key": p_apikey,
                "Content-Type": "application/json"
            }
        )
    # END MISSION SECTION
    except Exception as e:
        printusertext("ERROR 01: Unable to contact Meraki cloud")
        sys.exit(2)

    returnvalue = []
    if r.status_code != requests.codes.ok:
        returnvalue.append({"id": "null"})
        return returnvalue

    printusertext(r.text)
    rjson = r.json()

    return (rjson)

def getnwlist(p_apikey, p_orgid):
    # returns a list of all networks in an organization
    # on failure returns a single record with 'null' name and id

    time.sleep(API_EXEC_DELAY)
    try:
        # MISSION TODO
        r = requests.get(
            "MISSION: REPLACE WITH NETWORKS API CALL (in place of \
            Organization ID put %s)"
            % (p_orgid),
            headers={
                "X-Cisco-Meraki-API-Key": p_apikey,
                "Content-Type": "application/json"
            }
        )
    # END MISSION SECTION
    except Exception as e:
        printusertext("ERROR 05: Unable to contact Meraki cloud")
        sys.exit(2)

    printusertext(r.json)
    returnvalue = []
    if r.status_code != requests.codes.ok:
        returnvalue.append({"name": "null", "id": "null"})
        return (returnvalue)

    return (r.json())


def readmxfwruleset(p_apikey, p_nwid):
    # return the MX L3 firewall ruleset for a network

    time.sleep(API_EXEC_DELAY)
    try:
        # MISSION TODO
        r = requests.get(
            "MISSION: REPLACE WITH firewallrules API CALL (in place of \
            network ID put %s)"
            % (p_nwid),
            headers={
                "X-Cisco-Meraki-API-Key": p_apikey,
                "Content-Type": "application/json"
            }
        )
    # END MISSION SECTION
    except Exception as e:
        printusertext("ERROR 06: Unable to contact Meraki cloud")
        sys.exit(2)

    returnvalue = []
    if r.status_code != requests.codes.ok:
        returnvalue.append({"srcPort": "null"})
        return returnvalue

    rjson = r.json()

    return (rjson)


def printruleset(p_orgname, p_netname, p_ruleset):
    # Prints a single ruleset to stdout

    print("")
    print(
        'MX Firewall Ruleset for Organization "%s", Network "%s"'
        % (p_orgname, p_netname)
    )
    i = 1
    for line in p_ruleset:
        print(
            "LINE:%d protocol:%s, srcPort:%s, srcCidr:%s, destPort:%s, \
            destCidr:%s, policy:%s, syslogEnabled:%s, comment:%s"
            % (
                i,
                line["protocol"],
                line["srcPort"],
                line["srcCidr"],
                line["destPort"],
                line["destCidr"],
                line["policy"],
                line["syslogEnabled"],
                line["comment"],
            )
        )
        i += 1

    return (0)


def cmdprint(p_apikey, p_orglist):
    # Prints all rulesets in scope to stdout

    buffer = []

    for org in p_orglist:
        for net in org.nwdata:
            buffer = readmxfwruleset(p_apikey, net["id"])
            if buffer[0]["srcPort"] != "null":
                printruleset(org.name, net["name"], buffer)
            else:
                printusertext(
                    'WARNING: Unable to read MX ruleset for "%s" > "%s"'
                    % (org.name, net["name"])
                )

    return (0)


def formatfilename(p_orgname, p_netname):
    # make sure characters not suitable for filenames do not end up in string

    pattern = re.compile("([^\-_ \w])+")
    orgn = pattern.sub("", p_orgname)
    orgn = orgn.strip()
    netn = pattern.sub("", p_netname)
    netn = netn.strip()

    result = orgn + "__" + netn + ".txt"

    return (result)


def cmdcreatebackup(p_apikey, p_orglist):
    # code for the create-backup command

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
            flag_noerrors = False
        if flag_noerrors:
            flag_creationfailed = False
            break

    if flag_creationfailed:
        printusertext("ERROR 21: Unable to create directory for backups")
        sys.exit(2)
    else:
        printusertext('INFO: Backup directory is "%s"' % directory)

    buffer = []

    # create backups - one file per network
    for org in p_orglist:
        for net in org.nwdata:
            buffer = readmxfwruleset(p_apikey, net["id"])
            if buffer[0]["srcPort"] != "null":

                filename = formatfilename(org.name, net["name"])
                filepath = directory + "/" + filename
                if os.path.exists(filepath):
                    printusertext(
                        'ERROR 22: Cannot create backup file: name conflict \
                        "%s"'
                        % filename
                    )
                    sys.exit(2)
                else:
                    buffer = readmxfwruleset(p_apikey, net["id"])
                    try:
                        f = open(filepath, "w")
                    except Exception as e:
                        printusertext(
                            'ERROR 23: Unable to open file path for writing: \
                            "%s"'
                            % filepath
                        )
                        sys.exit(2)

                    for line in buffer:
                        f.write(
                            '{"protocol":"%s", "srcPort":"%s", "srcCidr":"%s", \
                            "destPort":"%s", "destCidr":"%s", "policy":"%s",\
                            "syslogEnabled":%s, "comment":"%s"}\n'
                            % (
                                line["protocol"],
                                line["srcPort"],
                                line["srcCidr"],
                                line["destPort"],
                                line["destCidr"],
                                line["policy"],
                                str(line["syslogEnabled"]).lower(),
                                line["comment"],
                            )
                        )

                    try:
                        f.close()
                    except Exception as e:
                        printusertext(
                            'ERROR 24: Unable to close file path: "%s"'
                            % filepath
                        )
                        sys.exit(2)

                    printusertext(
                        'INFO: Created backup for "%s". File: "%s"'
                        % (net["name"], filename)
                    )

                    spark.messages.create(
                        env_user.SPARK_ROOM_ID,
                        files=[filepath],
                        text="MISSION: L3 Rules Backup - Meraki - I have \
                        completed the mission!",
                    )

            else:
                printusertext(
                    'WARNING: Unable to read MX ruleset for "%s" > "%s"'
                    % (org.name, net["name"])
                )

    return (0)


def stripdefaultrule(p_inputruleset):
    # strips the default allow ending rule from an MX L3 Firewall ruleset
    outputset = []

    if len(p_inputruleset) > 0:
        lastline = p_inputruleset[len(p_inputruleset) - 1]
        if lastline == {
            "protocol": "Any",
            "policy": "allow",
            "comment": "Default rule",
            "srcCidr": "Any",
            "srcPort": "Any",
            "syslogEnabled": False,
            "destPort": "Any",
            "destCidr": "Any",
        }:
            outputset = p_inputruleset[:-1]
        else:
            outputset = p_inputruleset

    return (outputset)


def parsecommand(
    p_apikey, p_orglist, p_commandstr, p_flagcommit, p_flagbackup
):
    # parses command line argument "-c <command>"

    splitstr = p_commandstr.split(":")

    if len(splitstr) > 0:

        cmd = splitstr[0].strip()

        if cmd == "":
            # default command: print
            cmdprint(p_apikey, p_orglist)

        elif cmd == "print":
            cmdprint(p_apikey, p_orglist)

        elif cmd == "create-backup":
            cmdcreatebackup(p_apikey, p_orglist)

        else:
            printusertext('ERROR 44: Invalid command "%s"' % p_commandstr)
            sys.exit(2)

    else:
        printusertext("DEBUG: Command string parsing failed")
        sys.exit(2)

    return (0)


def main(argv):
    # python mxfirewallcontrol -k <key> -o <org> [-c <command>]

    # set default values for command line arguments
    arg_apikey = ""
    arg_command = ""

    # get command line arguments
    try:
        opts, args = getopt.getopt(argv, "hk:f:c:")
    except getopt.GetoptError:
        printhelp()
        sys.exit(2)

    for opt, arg in opts:
        if opt == "-h":
            printhelp()
            sys.exit()
        elif opt == "-k":
            arg_apikey = arg
        elif opt == "-c":
            arg_command = arg

    # check if all parameters are required parameters have been given
    if arg_apikey == "":
        printhelp()
        sys.exit(2)

    printusertext("INFO: Retrieving organization info")

    # compile list of organizations to be processed
    orglist = []
    orgjson = getorglist(arg_apikey)

    i = 0
    for record in orgjson:
        orglist.append(c_organizationdata())
        orglist[i].name = record["name"]
        orglist[i].id = record["id"]
        i += 1

    for org in orglist:
        netlist = getnwlist(arg_apikey,  org.id)
        org.nwdata = netlist

    # parse and execute command
    parsecommand(
        arg_apikey, orglist, arg_command, None, None
    )

    printusertext("INFO: End of script.")


if __name__ == "__main__":
    main(sys.argv[1:])
