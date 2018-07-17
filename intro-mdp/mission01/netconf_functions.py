"""This script configures GigabitEthernet2 interfaces on network devices.

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


from ncclient import manager
import xmltodict


def check_ip(device):
    """This function checks the IP configuration of GigabitEthernet2
    """
    # MISSION TODO 1: Provide the proper type of NETCONF object needed
    # Create an XML filter for targeted NETCONF queries
    netconf_filter = """
    <MISSION>
      <interfaces xmlns="http://openconfig.net/yang/interfaces">
        <interface>
            <name>GigabitEthernet2</name>
        </interface>
      </interfaces>
    </MISSION>"""
    # END MISSION SECTION

    # print("Opening NETCONF Connection to {}".format(device["conn"]["host"]))

    # Open a connection to the network device using ncclient
    with manager.connect(
        host=device["conn"]["host"],
        port=device["conn"]["netconf_port"],
        username=device["conn"]["username"],
        password=device["conn"]["password"],
        hostkey_verify=False,
    ) as m:

        # MISSION TODO 2: Provide the appropriate Manager Method Name
        # print("Sending a <get-config> operation to the device.\n")
        # Make a NETCONF <get-config> query using the filter
        netconf_reply = m.MISSION(source="running", filter=netconf_filter)
    # END MISSION SECTION

    # Uncomment the below lines to print the raw XML body
    # print("Here is the raw XML data returned from the device.\n")
    # print(xml.dom.minidom.parseString(netconf_reply.xml).toprettyxml())
    # print("")

    # Parse the returned XML to an Ordered Dictionary
    netconf_data = xmltodict.parse(netconf_reply.xml)["rpc-reply"]["data"]

    # Get the Interface Details
    interface = netconf_data["interfaces"]["interface"]

    print("Device: {}".format(device["conn"]["host"]))
    print("  Interface: {}".format(interface["config"]["name"]))
    try:
        ipv4 = interface["subinterfaces"]["subinterface"]["ipv4"]["addresses"][
            "address"
        ]
        print(
            "    IPv4: {}/{}".format(
                ipv4["ip"], ipv4["config"]["prefix-length"]
            )
        )
        return (
            device["conn"]["host"], ipv4["ip"], ipv4["config"]["prefix-length"]
        )

    except KeyError:
        print("    IPv4: not configured.")
    print("\n")


def set_ip(device):
    """This function configures the IP of GigabitEthernet2
    """
    # MISSION TODO 3: What XML attribute is used to indicate the capability?
    # Create an XML configuration template for openconfig-interfaces
    netconf_interface_template = """
    <config>
        <interfaces MISSION="http://openconfig.net/yang/interfaces">
            <interface>
                <name>{name}</name>
                <config>
                    <type
                     xmlns:ianaift="urn:ietf:params:xml:ns:yang:iana-if-type">
                        ianaift:ethernetCsmacd
                    </type>
                    <name>{name}</name>
                    <enabled>{status}</enabled>
                </config>
                <subinterfaces>
                    <subinterface>
                        <index>0</index>
                        <ipv4 xmlns="http://openconfig.net/yang/interfaces/ip">
                            <addresses>
                                <address>
                                    <ip>{ip_address}</ip>
                                    <config>
                                        <ip>{ip_address}</ip>
                                        <prefix-length>{prefix}</prefix-length>
                                    </config>
                                </address>
                            </addresses>
                        </ipv4>
                        <ipv6 xmlns="http://openconfig.net/yang/interfaces/ip">
                            <config>
                                <enabled>false</enabled>
                            </config>
                        </ipv6>
                    </subinterface>
                </subinterfaces>
            </interface>
        </interfaces>
    </config>"""
    # END MISSION SECTION

    # Create NETCONF Payload for device
    # MISSION TODO 4: What String method is used to fill in a template?
    netconf_data = netconf_interface_template.MISSION(
        name="GigabitEthernet2",
        status="true",
        ip_address=device["ip"],
        prefix=device["prefix"],
    )
    # END MISSION SECTION

    # Uncomment the below lines to view the config payload
    # print("The configuration payload to be sent over NETCONF.\n")
    # print(netconf_data)

    # Open a connection to the network device using ncclient
    with manager.connect(
        host=device["conn"]["host"],
        port=device["conn"]["netconf_port"],
        username=device["conn"]["username"],
        password=device["conn"]["password"],
        hostkey_verify=False,
    ) as m:

        # print("Sending a <edit-config> operation to the device.\n")
        # Make a NETCONF <get-config> query using the filter
        netconf_reply = m.edit_config(netconf_data, target="running")

        if netconf_reply.ok:
            print(
                "Device {} updated successfully".format(device["conn"]["host"])
            )
    print("")

    return netconf_reply


def clear_ip(device):
    """This function will clear the IP address on GigabitEthernet2
    """
    # MISSION TODO 5: What edit operation type is needed to clear details?
    # Create an XML configuration template for openconfig-interfaces
    netconf_interface_template = """
    <config>
        <interfaces xmlns="http://openconfig.net/yang/interfaces">
            <interface>
                <name>{name}</name>
                <subinterfaces>
                    <subinterface>
                        <index>0</index>
                        <ipv4 xmlns="http://openconfig.net/yang/interfaces/ip"
                            operation="MISSION" />
                        </ipv4>
                    </subinterface>
                </subinterfaces>
            </interface>
        </interfaces>
    </config>"""
    # END MISSION SECTION

    # Create NETCONF Payload for device
    netconf_data = netconf_interface_template.format(name="GigabitEthernet2")

    # Uncomment the below lines to view the config payload
    # print("The configuration payload to be sent over NETCONF.\n")
    # print(netconf_data)

    # MISSION TODO 6: What Manager method is used to start a session?
    # Open a connection to the network device using ncclient
    with manager.MISSION(
        host=device["conn"]["host"],
        port=device["conn"]["netconf_port"],
        username=device["conn"]["username"],
        password=device["conn"]["password"],
        hostkey_verify=False,
    ) as m:
        # END MISSION SECTION

        # print("Sending a <edit-config> operation to the device.\n")
        # Make a NETCONF <get-config> query using the filter
        netconf_reply = m.edit_config(netconf_data, target="running")

        if netconf_reply.ok:
            print(
                "Device {} updated successfully".format(device["conn"]["host"])
            )

    print("")

    return netconf_reply
