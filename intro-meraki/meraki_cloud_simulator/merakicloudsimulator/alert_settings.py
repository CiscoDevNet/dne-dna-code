http_servers = []
alert_settings = {
    "defaultDestinations": {
        "emails": [],
        "snmp": False,
        "allAdmins": False,
        "httpServerIds": []
    },
    "alerts": [
        {
            "type": "gatewayDown",
            "enabled": False,
            "alertDestinations": {
                "emails": [],
                "snmp": False,
                "allAdmins": False,
                "httpServerIds": []
            },
            "filters": {
                "timeout": 60
            }
        },
        {
            "type": "gatewayToRepeater",
            "enabled": False,
            "alertDestinations": {
                "emails": [],
                "snmp": False,
                "allAdmins": False,
                "httpServerIds": []
            },
            "filters": {}
        },
        {
            "type": "repeaterDown",
            "enabled": False,
            "alertDestinations": {
                "emails": [],
                "snmp": False,
                "allAdmins": False,
                "httpServerIds": []
            },
            "filters": {
                "timeout": 60
            }
        },
        {
            "type": "rogueAp",
            "enabled": False,
            "alertDestinations": {
                "emails": [],
                "snmp": False,
                "allAdmins": False,
                "httpServerIds": []
            },
            "filters": {}
        },
        {
            "type": "settingsChanged",
            "enabled": False,
            "alertDestinations": {
                "emails": [],
                "snmp": False,
                "allAdmins": False,
                "httpServerIds": []
            },
            "filters": {}
        },
        {
            "type": "vpnConnectivityChanged",
            "enabled": False,
            "alertDestinations": {
                "emails": [],
                "snmp": False,
                "allAdmins": False,
                "httpServerIds": []
            },
            "filters": {}
        },
        {
            "type": "usageAlert",
            "enabled": False,
            "alertDestinations": {
                "emails": [],
                "snmp": False,
                "allAdmins": False,
                "httpServerIds": []
            },
            "filters": {
                "threshold": 1,
                "period": 1200
            }
        },
        {
            "type": "ampMalwareDetected",
            "enabled": False,
            "alertDestinations": {
                "emails": [],
                "snmp": False,
                "allAdmins": False,
                "httpServerIds": []
            },
            "filters": {}
        },
        {
            "type": "ampMalwareBlocked",
            "enabled": False,
            "alertDestinations": {
                "emails": [],
                "snmp": False,
                "allAdmins": False,
                "httpServerIds": []
            },
            "filters": {}
        },
        {
            "type": "applianceDown",
            "enabled": False,
            "alertDestinations": {
                "emails": [],
                "snmp": False,
                "allAdmins": False,
                "httpServerIds": []
            },
            "filters": {
                "timeout": 5
            }
        },
        {
            "type": "failoverEvent",
            "enabled": False,
            "alertDestinations": {
                "emails": [],
                "snmp": False,
                "allAdmins": False,
                "httpServerIds": []
            },
            "filters": {}
        },
        {
            "type": "dhcpNoLeases",
            "enabled": False,
            "alertDestinations": {
                "emails": [],
                "snmp": False,
                "allAdmins": False,
                "httpServerIds": []
            },
            "filters": {}
        },
        {
            "type": "rogueDhcp",
            "enabled": False,
            "alertDestinations": {
                "emails": [],
                "snmp": False,
                "allAdmins": False,
                "httpServerIds": []
            },
            "filters": {}
        },
        {
            "type": "ipConflict",
            "enabled": False,
            "alertDestinations": {
                "emails": [],
                "snmp": False,
                "allAdmins": False,
                "httpServerIds": []
            },
            "filters": {}
        },
        {
            "type": "cellularUpDown",
            "enabled": False,
            "alertDestinations": {
                "emails": [],
                "snmp": False,
                "allAdmins": False,
                "httpServerIds": []
            },
            "filters": {}
        },
        {
            "type": "clientConnectivity",
            "enabled": False,
            "alertDestinations": {
                "emails": [],
                "snmp": False,
                "allAdmins": False,
                "httpServerIds": []
            },
            "filters": {
                "clients": []
            }
        },
        {
            "type": "vrrp",
            "enabled": False,
            "alertDestinations": {
                "emails": [],
                "snmp": False,
                "allAdmins": False,
                "httpServerIds": []
            },
            "filters": {}
        },
        {
            "type": "portDown",
            "enabled": False,
            "alertDestinations": {
                "emails": [],
                "snmp": False,
                "allAdmins": False,
                "httpServerIds": []
            },
            "filters": {
                "timeout": 5,
                "selector": "any port"
            }
        },
        {
            "type": "powerSupplyDown",
            "enabled": False,
            "alertDestinations": {
                "emails": [],
                "snmp": False,
                "allAdmins": False,
                "httpServerIds": []
            },
            "filters": {}
        },
        {
            "type": "rpsBackup",
            "enabled": False,
            "alertDestinations": {
                "emails": [],
                "snmp": False,
                "allAdmins": False,
                "httpServerIds": []
            },
            "filters": {}
        },
        {
            "type": "udldError",
            "enabled": False,
            "alertDestinations": {
                "emails": [],
                "snmp": False,
                "allAdmins": False,
                "httpServerIds": []
            },
            "filters": {}
        },
        {
            "type": "portError",
            "enabled": False,
            "alertDestinations": {
                "emails": [],
                "snmp": False,
                "allAdmins": False,
                "httpServerIds": []
            },
            "filters": {
                "selector": "any port"
            }
        },
        {
            "type": "portSpeed",
            "enabled": False,
            "alertDestinations": {
                "emails": [],
                "snmp": False,
                "allAdmins": False,
                "httpServerIds": []
            },
            "filters": {
                "selector": "any port"
            }
        },
        {
            "type": "newDhcpServer",
            "enabled": False,
            "alertDestinations": {
                "emails": [],
                "snmp": False,
                "allAdmins": False,
                "httpServerIds": []
            },
            "filters": {}
        },
        {
            "type": "switchDown",
            "enabled": False,
            "alertDestinations": {
                "emails": [],
                "snmp": False,
                "allAdmins": False,
                "httpServerIds": []
            },
            "filters": {
                "timeout": 5
            }
        },
        {
            "type": "nodeHardwareFailure",
            "enabled": False,
            "alertDestinations": {
                "emails": [],
                "snmp": False,
                "allAdmins": False,
                "httpServerIds": []
            },
            "filters": {}
        },
        {
            "type": "cameraDown",
            "enabled": False,
            "alertDestinations": {
                "emails": [],
                "snmp": False,
                "allAdmins": False,
                "httpServerIds": []
            },
            "filters": {
                "timeout": 60
            }
        }
    ]
}