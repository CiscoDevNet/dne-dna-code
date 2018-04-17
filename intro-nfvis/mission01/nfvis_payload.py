isr_payload = {
    "deployment": {
        "name": "ISRv",
		"vm_group": {
			"name": "ROUTER01",
			"image": "isrv-universalk9.16.06.02.tar.gz",
			"flavor": "ISRv-small",
			"bootup_time": 600,
			"recovery_wait_time": 0,
			"interfaces": {
				"interface": [{
					"nicid": 0,
					"network": "int-mgmt-net"
					},
					{
					"nicid": 1,
					"network": "wan-net"
					},
					{
					"nicid": 2,
					"network": "svc-net"
					}
				]
			},
			"kpi_data": {
				"kpi": {
					"event_name": "VM_ALIVE",
					"metric_value": "1",
					"metric_cond": "GT",
					"metric_type": "UINT32",
					"metric_collector": {
						"type": "ICMPPing",
						"nicid": 0,
						"poll_frequency": 3,
						"polling_unit": "seconds",
						"continuous_alarm": "false"
					}
				}
			},
			"rules": {
				"admin_rules": {
					"rule": {
						"event_name": "VM_ALIVE",
						"action": [
							"ALWAYS log",
							"FALSE recover autohealing",
							"TRUE servicebooted.sh"
						]
					}
				}
			},
			"config_data": {
				"configuration": {
					"dst": "bootstrap_config",
					"variable": [{
						"name": "HOST_NAME",
						"val": "Pod1-ISRv"
						},
						{
						"name": "LOOPBACK_IP",
						"val": "10.255.255.1"
						},
						{
						"name": "WAN_IP",
						"val": "10.10.100.1"
						},
						{
						"name": "TECH_PACKAGE",
						"val": "ax"
						},
						{
						"name": "LAN_IP",
						"val": "10.1.1.1"
						},
						{
						"name": "MGMT_IP",
						"val": "10.11.1.1"
						}
					]
				}
			}
		}
	}
}

asa_payload = {
    "deployment": {
        "name": "ASAv",
		"vm_group": {
			"name": "ASA01",
			"image": "asav961.tar.gz",
			"flavor": "ASAv10",
			"bootup_time": 600,
			"recovery_wait_time": 0,
			"interfaces": {
				"interface": [{
					"nicid": 0,
					"network": "int-mgmt-net"
					},
					{
					"nicid": 1,
					"network": "svc-net"
					},
					{
					"nicid": 2,
					"network": "lan-net"
					}
				]
			},
			"kpi_data": {
				"kpi": {
					"event_name": "VM_ALIVE",
					"metric_value": "1",
					"metric_cond": "GT",
					"metric_type": "UINT32",
					"metric_collector": {
						"type": "ICMPPing",
						"nicid": 0,
						"poll_frequency": 3,
						"polling_unit": "seconds",
						"continuous_alarm": "false"
					}
				}
			},
			"rules": {
				"admin_rules": {
					"rule": {
						"event_name": "VM_ALIVE",
						"action": [
							"ALWAYS log",
							"FALSE recover autohealing",
							"TRUE servicebooted.sh"
						]
					}
				}
			},
			"config_data": {
				"configuration": {
					"dst": "bootstrap_config",
					"variable": [{
						"name": "HOST_NAME",
						"val": "Pod1-ISRv"
						},
						{
						"name": "LOOPBACK_IP",
						"val": "10.255.255.1"
						},
						{
						"name": "WAN_IP",
						"val": "10.10.100.1"
						},
						{
						"name": "LAN_IP",
						"val": "10.1.1.1"
						},
						{
						"name": "MGMT_IP",
						"val": "10.11.1.1"
						}
					]
				}
			}
		}
	}
}
