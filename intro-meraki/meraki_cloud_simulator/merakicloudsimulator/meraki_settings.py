ORGANIZATIONS = [{"id": "1234567", "name": "Simulated Organization"}]

# Networks indexed by organization ID.
NETWORKS = {
    "1234567": [
        {
            "id": "L_12345678910",
            "organizationId": "1234567",
            "name": "Simulated Network",
            "timeZone": "America/New_York",
            "tags": "",
            "productTypes": ["appliance", "switch", "wireless"],
            "type": "combined",
            "disableMyMerakiCom": False,
            "disableRemoteStatusPage": True,
        }
    ]
}