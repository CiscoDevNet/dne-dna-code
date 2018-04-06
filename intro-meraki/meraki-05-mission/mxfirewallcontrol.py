# This is a script to manage firewall rulesets, by backing them up, inserting new rules or replacing the
#  whole ruleset.
#
# To run the script, enter:
#  python mxfirewallcontrol.py -k <key> -o <org> [-f <filter>] [-c <command>] [-m <mode>]
#
# Mandatory arguments:
#  -k <key>     : Your Meraki Dashboard API key
#  -o <org>     : The name of the Meraki dashboard organization you want to process. Enter "/all" for all
#
# Optional arguments:
#  -f <filter>   : Define a subset of networks or templates to be processed. To use multiple filters,
#                   separate them with commas. A network/template needs to satisfy all filters to be processed.
#                   Valid options:
#                  -f name:<name>               Network/template name must match <name>. Use * for wildcard.
#                                                Wildcard character only allowed in beginning or end of string
#                  -f tag:<tag>                 Network tags must include <tag>
#                  -f type:network              Process only non-template networks
#                  -f type:template             Process only configuration templates (default filter)
#                  -f type:any                  Process both networks and config templates. Cannot be combined
#                                                with tag filters
# -c <command>   : Specify the operation to be carried out. When specifying rule numbers, a positive number
#                                                indicates counting from top to bottom. First rule is "1".
#                                                A negative number  indicates counting from bottom to top.
#                                                Last rule is "-1". Valid options:
#                  -c print                     Do not make changes, just print the ruleset to screen (default)
#                  -c create-backup             Save rulesets in folder mxfirewallctl_backup_<timestamp> as
#                                                filenames "<org name>__<net name>.txt"
#
# To make script chaining easier, all lines containing informational messages to the user
#  start with the character @
#
# The full manual for this script can be found here:
#   https://github.com/meraki/automation-scripts/blob/master/mxfirewallcontrol_manual.pdf


import sys, getopt, requests, json, time, datetime, os, re

class c_organizationdata:
    def __init__(self):
        self.name      = ''
        self.id        = ''
        self.nwdata    = [] #List of dictionaries as returned by cloud. Primary key is 'id'
#end class

class c_filter:
    def __init__(self):
        self.type      = ''
        self.value     = ''
#end class

#Used for time.sleep(API_EXEC_DELAY). Delay added to avoid hitting dashboard API max request rate
API_EXEC_DELAY = 0.21

def printusertext(p_message):
    #prints a line of text that is meant for the user to read
    #do not process these lines when chaining scripts
    print('@ %s' % p_message)


def printhelp():
    #prints help text

    printusertext('This is a script to manage firewall rulesets, by backing them up, inserting new rules')
    printusertext('or replacing the whole ruleset.')
    printusertext('')
    printusertext('To run the script, enter:')
    printusertext('python mxfirewallcontrol.py -k <key> -o <org> [-f <filter>] [-c <command>] [-m <mode>]')
    printusertext('')
    printusertext('Mandatory arguments:')
    printusertext('  -k <key>     : Your Meraki Dashboard API key')
    printusertext('  -o <org>     : The name of the Meraki dashboard organization you want to process. Enter /all for all')
    printusertext('')
    printusertext('Optional arguments:')
    printusertext('  -f <filter>  : Define a subset of networks or templates to be processed. Valid options:')
    printusertext('                  -f name:<name>               Network/template name must match <name>. Use * for wildcard.')
    printusertext('                  -f tag:<tag>                 Network tags must include <tag>. Cannot be used with templates')
    printusertext('                  -f type:network              Process only non-template networks')
    printusertext('                  -f type:template             Process only configuration templates (default filter)')
    printusertext('                  -f type:any                  Process both networks and config templates.')
    printusertext('                                                Cannot be combined with tag filters')
    printusertext(' -c <command>   : Specify the operation to be carried out. When specifying rule numbers, a positive number')
    printusertext('                   indicates counting from top to bottom. First rule is "1". A negative number')
    printusertext('                   indicates counting from bottom to top. Last rule is "-1". Valid options:')
    printusertext('                  -c print                     Do not make changes, just print the ruleset to screen (default)')
    printusertext('                  -c create-backup             Save rulesets in folder mxfirewallctl_backup_<timestamp> as')
    printusertext('                                                filenames "<org name>__<net name>.txt"')

    printusertext('')
    printusertext('Use double quotes ("") in Windows to pass arguments containing spaces. Names are case-sensitive.')


def getorglist(p_apikey):
    #returns the organizations' list for a specified admin

    time.sleep(API_EXEC_DELAY)
    try:
        r = requests.get('https://api.meraki.com/api/v0/organizations', headers={'X-Cisco-Meraki-API-Key': p_apikey, 'Content-Type': 'application/json'})
    except:
        printusertext('ERROR 01: Unable to contact Meraki cloud')
        sys.exit(2)

    returnvalue = []
    if r.status_code != requests.codes.ok:
        returnvalue.append({'id':'null'})
        return returnvalue

    printusertext(r.text)
    rjson = r.json()

    return(rjson)


def getorgid(p_apikey, p_orgname):
    #looks up org id for a specific org name
    #on failure returns 'null'

    time.sleep(API_EXEC_DELAY)
    try:
        r = requests.get('https://api.meraki.com/api/v0/organizations', headers={'X-Cisco-Meraki-API-Key': p_apikey, 'Content-Type': 'application/json'})
    except:
        printusertext('ERROR 02: Unable to contact Meraki cloud')
        sys.exit(2)

    if r.status_code != requests.codes.ok:
        return 'null'

    rjson = r.json()

    for record in rjson:
        if record['name'] == p_orgname:
            return record['id']
    return('null')



def getnwlist(p_apikey,p_orgid):
    #returns a list of all networks in an organization
    #on failure returns a single record with 'null' name and id

    time.sleep(API_EXEC_DELAY)
    try:
        r = requests.get('https://api.meraki.com/api/v0/organizations/%s/networks' % (p_orgid), headers={'X-Cisco-Meraki-API-Key': p_apikey, 'Content-Type': 'application/json'})
    except:
        printusertext('ERROR 05: Unable to contact Meraki cloud')
        sys.exit(2)


    printusertext(r.json)
    returnvalue = []
    if r.status_code != requests.codes.ok:
        returnvalue.append({'name': 'null', 'id': 'null'})
        return(returnvalue)

    return(r.json())


def readmxfwruleset(p_apikey,  p_nwid):
    #return the MX L3 firewall ruleset for a network

    time.sleep(API_EXEC_DELAY)
    try:
        r = requests.get('https://api.meraki.com/api/v0/networks/%s/firewallrules' % (p_nwid), headers={'X-Cisco-Meraki-API-Key': p_apikey, 'Content-Type': 'application/json'})
    except:
        printusertext('ERROR 06: Unable to contact Meraki cloud')
        sys.exit(2)

    returnvalue = []
    if r.status_code != requests.codes.ok:
        returnvalue.append({'srcPort':'null'})
        return returnvalue

    rjson = r.json()

    return(rjson)


def filternetworks (p_apikey,  p_orgid, p_filters):
    #returns list of networks and/or templates within the scope of "p_filters"

    #NOTE: THE DEFAULT FILTER SCOPE OF THIS SCRIPT SELECTS CONFIG TEMPLATES BUT NOT NETWORKS
    #      IF NO TYPE FILTER IS APPLIED AT EXECUTION TIME. MODIFY THE LINES BELOW TO CHANGE THIS

    #TODO: Evaluate if handling default filter needs to be rearchitected to a more change-friendly form

    flag_getnetworks    = True
    rawnetlist          = []
    rawtemplist         = []
    filteredlist        = []

    #list of filters by type
    count_namefilters   = 0
    filter_namebegins   = []
    filter_namecontains = []
    filter_nameends     = []
    filter_nameequals   = []
    filter_tag          = []

    for item in p_filters:
        if   item.type == 'type':
            if   item.value == 'network':
                flag_getnetworks  = True
        elif item.type == 'name_begins':
            filter_namebegins.append(item.value)
            count_namefilters += 1
        elif item.type == 'name_contains':
            filter_namecontains.append(item.value)
            count_namefilters += 1
        elif item.type == 'name_ends':
            filter_nameends.append(item.value)
            count_namefilters += 1
        elif item.type == 'name_equals':
            filter_nameequals.append(item.value)
            count_namefilters += 1
        elif item.type == 'tag':
            filter_tag.append(item.value)

    if flag_getnetworks:
        rawnetlist = getnwlist(p_apikey,  p_orgid)
        if len(rawnetlist) > 0:
            if rawnetlist[0]['id'] == 'null':
                printusertext('ERROR 08: Unable to get network list from Meraki cloud')
                sys.exit(2)

    #process tag filters now, since they are incompatible with config templates
    #transfer networks to next level of processing only if they satisfy tag requirements
    buffer1  = []
    tagflags = []

    if len(filter_tag) > 0:
        #set all flags to do_transfer
        for net in rawnetlist:
            tagflags.append(True)
            #examine tag incompliance and flag do_not_transfer accordingly
            for filter in filter_tag:
                if type(net['tags']) is str:
                    if net['tags'].find(filter) == -1:
                        tagflags[len(tagflags)-1] = False
                else:
                    tagflags[len(tagflags)-1] = False

        #copy flagged nets
        for net, flag in zip(rawnetlist, tagflags):
            if flag:
                buffer1.append(net)

    else: #no tag filters given, just send everything to next processing stage
        buffer1 += rawnetlist



    #process name filters
    nameflags = []
    buffer2   = []
    if count_namefilters > 0:
        for net in buffer1:
            #flag all as compliant
            nameflags.append(True)
            #loop through filter lists and flag as incompliant as needed
            for fnb in filter_namebegins:
                if not net['name'].startswith(fnb):
                    nameflags[len(nameflags)-1] = False
            for fnc in filter_namecontains:
                if net['name'].find(fnc) == -1:
                    nameflags[len(nameflags)-1] = False
            for fnd in filter_nameends:
                if not net['name'].endswith(fnd):
                    nameflags[len(nameflags)-1] = False
            for fnq in filter_nameequals:
                if not net['name'] == fnq:
                    nameflags[len(nameflags)-1] = False
        for net, flag in zip(buffer1, nameflags):
            if flag:
                buffer2.append(net)
    else:
        buffer2 += buffer1

    return(buffer2)


def parsefilter(p_string):
    #parses filter command line argument
    processed        = []
    flag_gotname     = False
    flag_gottype     = False
    flag_gottag      = False
    flag_gotall      = False
    flag_gotnetwork  = False
    flag_gottemplate = False
    flag_defaulttype = True

    if len(p_string) == 0:
        return('')

    inputfilters = p_string.split(',')

    for item in inputfilters:
        splititem = item.split(':')
        if len(splititem) == 2 and not flag_gotall:
            ftype  = splititem[0].strip()
            fvalue = splititem[1].strip()

            #process wildcards
            if ftype == 'name':
                if len(fvalue) > 0:
                    if fvalue.endswith('*'):
                        if fvalue.startswith('*'):
                            #search for extra *
                            ftype  = 'name_contains'
                            fvalue = fvalue[1:-1]
                        else:
                            ftype = 'name_begins'
                            fvalue = fvalue[:-1]
                    elif fvalue.startswith('*'):
                        ftype = 'name_ends'
                        fvalue = fvalue[1:]
                    else:
                        ftype = 'name_equals'
                else: #len(fvalue) <= 0
                    printusertext('ERROR 10: Invalid filter "%s"' % item)
                    sys.exit(2)
            elif ftype == 'tag':
                if len(fvalue) == 0:
                    printusertext('ERROR 11: Invalid filter "%s"' % item)
                    sys.exit(2)
                elif flag_gottemplate:
                    printusertext('ERROR 12: Filter "%s" cannot be combined with type:template or type:any' % item)
                    sys.exit(2)
                flag_gottag = True
            elif ftype == 'type':
                if flag_gottype:
                    printusertext('ERROR 13: Filter "type" can only be used once: "%s"' % p_string)
                    sys.exit(2)
                if fvalue   == 'network':
                    flag_gotnetwork  = True
                    flag_defaulttype = False
                elif fvalue == 'template':
                    if flag_gottag:
                        printusertext('ERROR 14: Filter "tag" cannot be used with filter "type:template"')
                        sys.exit(2)
                    flag_gottemplate = True
                elif fvalue == 'any':
                    if flag_gottag:
                        printusertext('ERROR 15: Filter "tag" cannot be used with filter "type:any"')
                        sys.exit(2)
                    flag_gottemplate = True
                    flag_gotnetwork  = True
                else:
                    printusertext('ERROR 16: Invalid filter "%s"' % item)
                    sys.exit(2)
                flag_gottype = True
            else:
                printusertext('ERROR 17: Invalid filter "%s"' % item)
                sys.exit(2)
            #check for invalid wildcards regardless of filter type
            if '*' in fvalue:
                printusertext('ERROR 18: Invalid use of wildcard in filter "%s"' % item)
                sys.exit(2)

            processed.append(c_filter())
            processed[len(processed)-1].type  = ftype
            processed[len(processed)-1].value = fvalue
        else:
            printusertext('ERROR 19: Invalid filter string "%s"' % p_string)
            sys.exit(2)

    #check for filter incompatibilities with default type-filter, if it has not been changed
    if flag_defaulttype and flag_gottag:
        printusertext('ERROR 20: Default type filter is "template". Filter "tag" needs filter "type:network"')
        sys.exit(2)

    return (processed)


def printruleset(p_orgname, p_netname, p_ruleset):
    #Prints a single ruleset to stdout

    print('')
    print('MX Firewall Ruleset for Organization "%s", Network "%s"' % (p_orgname, p_netname))
    i = 1
    for line in p_ruleset:
        print('LINE:%d protocol:%s, srcPort:%s, srcCidr:%s, destPort:%s, destCidr:%s, policy:%s, syslogEnabled:%s, comment:%s' % (i,line['protocol'],line['srcPort'],line['srcCidr'],line['destPort'],line['destCidr'],line['policy'],line['syslogEnabled'],line['comment']))
        i += 1

    return(0)


def cmdprint(p_apikey, p_orglist):
    #Prints all rulesets in scope to stdout

    buffer = []

    for org in p_orglist:
        for net in org.nwdata:
            buffer = readmxfwruleset(p_apikey, net['id'])
            if buffer[0]['srcPort'] != 'null':
                printruleset(org.name, net['name'], buffer)
            else:
                printusertext('WARNING: Unable to read MX ruleset for "%s" > "%s"' % (org.name,net['name']))

    return(0)


def formatfilename(p_orgname, p_netname):
    #make sure characters not suitable for filenames do not end up in string

    pattern = re.compile('([^\-_ \w])+')
    orgn    = pattern.sub('', p_orgname)
    orgn    = orgn.strip()
    netn    = pattern.sub('', p_netname)
    netn    = netn.strip()

    result  = orgn + '__' + netn + '.txt'

    return (result)


def cmdcreatebackup(p_apikey, p_orglist):
    #code for the create-backup command

    #create directory to place backups
    flag_creationfailed = True
    MAX_FOLDER_CREATE_TRIES = 5
    for i in range (0, MAX_FOLDER_CREATE_TRIES):
        time.sleep(2)
        timestamp = '{:%Y%m%d_%H%M%S}'.format(datetime.datetime.now())
        directory = 'mxfwctl_backup_' + timestamp
        flag_noerrors = True
        try:
            os.makedirs(directory)
        except:
            flag_noerrors = False
        if flag_noerrors:
            flag_creationfailed = False
            break
    if flag_creationfailed:
        printusertext('ERROR 21: Unable to create directory for backups')
        sys.exit(2)
    else:
        printusertext('INFO: Backup directory is "%s"' % directory)

    buffer = []

    #create backups - one file per network
    for org in p_orglist:
        for net in org.nwdata:
            buffer = readmxfwruleset(p_apikey, net['id'])
            if buffer[0]['srcPort'] != 'null':

                filename = formatfilename(org.name, net['name'])
                filepath = directory + '/' + filename
                if os.path.exists(filepath):
                    printusertext('ERROR 22: Cannot create backup file: name conflict "%s"' % filename)
                    sys.exit(2)
                else:
                    buffer = readmxfwruleset(p_apikey, net['id'])
                    try:
                        f = open(filepath, 'w')
                    except:
                        printusertext('ERROR 23: Unable to open file path for writing: "%s"' % filepath)
                        sys.exit(2)

                    for line in buffer:
                        f.write('{"protocol":"%s", "srcPort":"%s", "srcCidr":"%s", "destPort":"%s", "destCidr":"%s", "policy":"%s", "syslogEnabled":%s, "comment":"%s"}\n' % (line['protocol'],line['srcPort'],line['srcCidr'],line['destPort'],line['destCidr'],line['policy'],str(line['syslogEnabled']).lower(),line['comment']))

                    try:
                        f.close()
                    except:
                        printusertext('ERROR 24: Unable to close file path: "%s"' % filepath)
                        sys.exit(2)

                    printusertext('INFO: Created backup for "%s". File: "%s"' % (net['name'], filename))

                    m = MultipartEncoder({'roomId': 'Y2lzY2.....',
                                          'text': 'L3 Rules Backup',
                                          'files': (filename, open('filename', 'rb'),
                                          'image/png')})

                    r = requests.post('https://api.ciscospark.com/v1/messages', data=m,
                                      headers={'Authorization': 'Bearer ACCESS_TOKEN',
                                      'Content-Type': m.content_type})

                    print r.text


            else:
                printusertext('WARNING: Unable to read MX ruleset for "%s" > "%s"' % (org.name,net['name']))

    return(0)

def stripdefaultrule(p_inputruleset):
    #strips the default allow ending rule from an MX L3 Firewall ruleset
    outputset = []

    if len(p_inputruleset) > 0:
        lastline = p_inputruleset[len(p_inputruleset)-1]
        if lastline == {'protocol': 'Any', 'policy': 'allow', 'comment': 'Default rule', 'srcCidr': 'Any', 'srcPort': 'Any', 'syslogEnabled': False, 'destPort': 'Any', 'destCidr': 'Any'}:
            outputset = p_inputruleset[:-1]
        else:
            outputset = p_inputruleset

    return(outputset)


def loadruleset(p_filepath):
    #Load a ruleset from file to memory. Drop default allow rules
    ruleset = []
    jdump = '['

    try:
        f = open(p_filepath, 'r')
    except:
        printusertext('ERROR 25: Unable to open file path for reading: "%s"' % p_filepath)
        sys.exit(2)

    for line in f:
        try:
            buffer = line
        except:
            printusertext('ERROR 26: Unable to read from file: "%s"' % p_filepath)
            sys.exit(2)

        if len(buffer.strip())>1:
            if not jdump.endswith('['):
                jdump += ','
            jdump += buffer[:-1]

    try:
        f.close()
    except:
        printusertext('ERROR 27: Unable to close input file "%s"' % p_filepath)
        sys.exit(2)

    jdump += ']'

    try:
        ruleset = json.loads(jdump)
    except:
        printusertext('ERROR 28: Invalid input file format "%s"' % p_filepath)
        sys.exit(2)

    ruleset = stripdefaultrule(ruleset)

    return(ruleset)



def parsecommand(p_apikey, p_orglist, p_commandstr, p_flagcommit, p_flagbackup):
    #parses command line argument "-c <command>"

    splitstr = p_commandstr.split(':')

    if len(splitstr) > 0:

        cmd = splitstr[0].strip()

        if   cmd == '':
            #default command: print
            cmdprint(p_apikey, p_orglist)

        elif cmd == 'print':
            cmdprint(p_apikey, p_orglist)

        elif cmd == 'create-backup':
            cmdcreatebackup(p_apikey, p_orglist)

        else:
            printusertext('ERROR 44: Invalid command "%s"' % p_commandstr)
            sys.exit(2)

    else:
        printusertext('DEBUG: Command string parsing failed')
        sys.exit(2)

    return (0)


def main(argv):
    #python mxfirewallcontrol -k <key> -o <org> [-f <filter>] [-c <command>] [-m <mode>]

    #set default values for command line arguments
    arg_apikey  = ''
    arg_org     = ''
    arg_filter  = ''
    arg_command = ''
    arg_mode    = 'simulation'

    #get command line arguments
    try:
        opts, args = getopt.getopt(argv, 'hk:o:f:c:m:')
    except getopt.GetoptError:
        printhelp()
        sys.exit(2)

    for opt, arg in opts:
        if   opt == '-h':
            printhelp()
            sys.exit()
        elif opt == '-k':
            arg_apikey  = arg
        elif opt == '-o':
            arg_org     = arg
        elif opt == '-f':
            arg_filter   = arg
        elif opt == '-c':
            arg_command = arg
        elif opt == '-m':
            arg_mode    = arg

    #check if all parameters are required parameters have been given
    if arg_apikey == '' or arg_org == '':
        printhelp()
        sys.exit(2)

    #set flags
    flag_defaultscope       = False
    if arg_filter   == '':
        flag_defaultscope   = True

    flag_defaultcommand     = False
    if arg_command == '':
        flag_defaultcommand = True

    flag_invalidmode        = True
    flag_modecommit         = False
    flag_modebackup         = True
    if arg_mode    == '':
        flag_invalidmode    = False
    elif arg_mode  == 'simulation':
        flag_invalidmode    = False
    elif arg_mode  == 'commit':
        flag_modecommit     = True
        flag_invalidmode    = False
    elif arg_mode  == 'commit-no-backup':
        flag_modecommit     = True
        flag_modebackup     = False
        flag_invalidmode    = False


    if flag_invalidmode:
        printusertext('ERROR 45: Argument -m <mode> is invalid')
        sys.exit(2)

    printusertext('INFO: Retrieving organization info')

    #compile list of organizations to be processed
    orglist = []
    if arg_org == '/all':
        orgjson = getorglist(arg_apikey)

        i = 0
        for record in orgjson:
            orglist.append(c_organizationdata())
            orglist[i].name = record['name']
            orglist[i].id   = record['id']
            i += 1

    else:
        orglist.append(c_organizationdata())
        orglist[0].name = arg_org
        orglist[0].id   = getorgid(arg_apikey, arg_org)
        if orglist[0].id == 'null':
            printusertext('ERROR 46: Fetching source organization ID failed')
            sys.exit(2)

    #parse filter argument
    filters = parsefilter(arg_filter)

    #compile filtered networks' list
    for org in orglist:
        filterednwlist = filternetworks(arg_apikey, org.id, filters)
        org.nwdata = filterednwlist

    #parse and execute command
    parsecommand(arg_apikey, orglist, arg_command, flag_modecommit, flag_modebackup)

    printusertext('INFO: End of script.')

if __name__ == '__main__':
    main(sys.argv[1:])
