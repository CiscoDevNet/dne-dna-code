"""Cisco Meraki Cloud Simulator for External Captive Portal labs."""
from merakicloudsimulator import merakicloudsimulator
from merakicloudsimulator.alert_settings import alert_settings, http_servers
from merakicloudsimulator.sample_alert_messages import alert_messages
from merakicloudsimulator.meraki_settings import ORGANIZATIONS, NETWORKS
from flask import request, render_template, redirect, jsonify, abort
import string
import requests
import random
import json
from datetime import datetime
from time import sleep
import threading

stop_alert_thread = False
alert_thread = threading.Thread() 


def post_webhook_alerts():
    try:
        while True:
            global stop_alert_thread
            if stop_alert_thread:
                print("Stopping Posting of Alerts Stream")
                break
            for alert in alert_settings["alerts"]:
                if stop_alert_thread:
                    print("Stopping Posting of Alerts Individual Alerts")
                    break
                if alert["enabled"] == True:
                    alert_message = alert_messages[alert["type"]]
                    for http_server in http_servers:
                        alert_message["sharedSecret"] = http_server["sharedSecret"]
                        alert_message["organizationId"] = ORGANIZATIONS[0]["id"]
                        alert_message["organizationName"] = ORGANIZATIONS[0]["name"]
                        alert_message["networkId"] = NETWORKS[ORGANIZATIONS[0]["id"]][0]["id"]
                        alert_message["networkName"] = NETWORKS[ORGANIZATIONS[0]["id"]][0]["name"]
                        alert_message["alertId"] = ''.join([random.choice(string.digits) for n in range(16)])
                        alert_message["sentAt"] = datetime.now().isoformat(sep='T')
                        alert_message["occurredAt"] = datetime.now().isoformat(sep='T')
                        requests.post(http_servers[0]["url"], json=alert_message)
                        sleep(10)
    except Exception as e:
        print(e)
        abort(500)


def manage_alert_streaming_thread():
    global alert_thread
    global stop_alert_thread

    try:
        if alert_thread.isAlive():
            print("alert thread already started, killing an restarting")
            stop_alert_thread = True
            alert_thread.join()
            print('alert_thread killed')
            stop_alert_thread = False
            alert_thread = threading.Thread(target = post_webhook_alerts, daemon=True) 
            alert_thread.start()
        else:
            print('alert thread not started; starting...')
            stop_alert_thread = False
            alert_thread = threading.Thread(target = post_webhook_alerts, daemon=True) 
            alert_thread.start()
    except Exception as e:
        print(e)
        abort(500)

# Helper Functions
def generate_fake_http_server_id():
    """Generate a fake http_server_id."""
    return ''.join([random.choice(string.ascii_letters + string.digits) for n in range(36)])


# Flask micro-webservice API/URI endpoints
@merakicloudsimulator.route("/networks/<network_id>/httpServers", methods=["GET"])
def get_http_servers(network_id):
    """Simulate getting httpServers configurations."""
    print(f"Getting httpServers for {network_id}.")
    return jsonify(http_servers)

@merakicloudsimulator.route("/networks/<network_id>/httpServers", methods=["POST"])
def post_httpServers(network_id):
    """Simulate setting httpServers configurations."""
    print(f"Settings updated for network {network_id}.")
    try:
        new_server = request.json
        new_server_keys = new_server.keys()
        if "name" in new_server_keys and "url" in new_server_keys and "sharedSecret" in new_server_keys:
            new_server["id"] = generate_fake_http_server_id()
            new_server["networkId"] = network_id
            http_servers.append(new_server)
            return jsonify(new_server), 201
        else:
            abort(400)
    except Exception as e:
        print(e)
        abort(400)


@merakicloudsimulator.route("/networks/<network_id>/alertSettings",
    methods=["GET"],
)
def get_alert_settings(network_id):
    """Simulate getting alertSettings configurations."""
    print(f"Getting alertSettings for {network_id}.")
    return jsonify(alert_settings)

@merakicloudsimulator.route("/networks/<network_id>/alertSettings",
    methods=["PUT"],
)
def put_alert_settings(network_id):
    global alert_thread
    global stop_alert_thread

    try:
            
        destination_set = False
        alert_set = False
        """Simulate setting alertSettings configurations."""
        print(f"Setting alertSettings for {network_id}.")
        new_settings = request.json
        new_settings_keys = new_settings.keys()
        if "defaultDestinations" in new_settings_keys or "alerts" in new_settings_keys:
            if "defaultDestinations" in new_settings_keys:
                defaultDestinations_keys = new_settings["defaultDestinations"].keys()
                if "httpServerIds" in defaultDestinations_keys:
                    alert_settings["defaultDestinations"]["httpServerIds"].clear()
                    if len(new_settings["defaultDestinations"]["httpServerIds"]) > 0:
                        alert_settings["defaultDestinations"]["httpServerIds"].append(new_settings["defaultDestinations"]["httpServerIds"][0])
                        destination_set = True
                else:
                    abort(400)
            if "alerts" in new_settings_keys:
                for new_alert in new_settings["alerts"]:
                    alert_keys = new_alert.keys()
                    if "enabled" in alert_keys and "type" in alert_keys:
                        alert_index = next((index for (index, alert) in enumerate(alert_settings["alerts"]) if alert["type"] == new_alert["type"]), None)
                        alert_settings["alerts"][alert_index] = new_alert
                        alert_set = True
                    else:
                        abort(400)
        else:
            abort(400)

        if destination_set and alert_set:
            manage_alert_streaming_thread()

        return jsonify(alert_settings)
    except Exception as e:
        print(e)
        abort(400)


@merakicloudsimulator.route("/webhook", methods=["POST","GET"])
def webhooksettings():
    try:
        if request.method == 'POST':
            webhook_server_name = request.form["server_name"].lstrip().rstrip()
            webhook_server_url  = request.form["server_url"].lstrip().rstrip()
            webhook_shared_secret = request.form["shared_secret"].lstrip().rstrip()
            webhook_default_destination = request.form.getlist("default_destination")
            
            if webhook_shared_secret != "" and webhook_server_name != "" and webhook_server_url != "":
                http_servers.clear()
                http_servers.append({
                    "name": webhook_server_name,
                    "url": webhook_server_url,
                    "sharedSecret": webhook_shared_secret,
                    "id": generate_fake_http_server_id(),
                    "networkId": NETWORKS[ORGANIZATIONS[0]["id"]][0]["id"]
                })
                print(f"Alert webhook receiver added: \n{http_servers}")

            if len(webhook_default_destination) > 0 and len(http_servers) > 0:
                alert_settings["defaultDestinations"]["httpServerIds"].clear()
                alert_settings["defaultDestinations"]["httpServerIds"].\
                append(http_servers[0]["id"])
                print(f"Alert Destination Changed in GUI")

            webhook_checked_settings = request.form.getlist("checked_settings")
            for alert in alert_settings['alerts']:
                if alert["type"] in webhook_checked_settings:
                    alert["enabled"] = True
                else:
                    alert["enabled"] = False

            print(f"Alert Settings Changed in GUI: {alert_settings['alerts']}")
            if len(webhook_default_destination) > 0 and len(http_servers) > 0 and len(webhook_checked_settings) > 0:
                manage_alert_streaming_thread()
        else:
            if len(http_servers) > 0:
                webhook_server_name = http_servers[0]["name"]
                webhook_server_url = http_servers[0]["url"]
                webhook_shared_secret = http_servers[0]["sharedSecret"]
            else:
                webhook_server_name = ""
                webhook_server_url = ""
                webhook_shared_secret = ""

            print(alert_settings["alerts"])
            webhook_checked_settings = []
            for alert in alert_settings["alerts"]:
                if alert["enabled"]:
                    webhook_checked_settings.append(alert["type"])
            
            webhook_default_destination = []
            if len(alert_settings["defaultDestinations"]["httpServerIds"]) > 0:
                webhook_default_destination.append("default_destination")
        

        return render_template("webhook.html", \
        checked_settings=webhook_checked_settings, server_name=webhook_server_name, \
        server_url=webhook_server_url, shared_secret=webhook_shared_secret, \
        default_destination=webhook_default_destination)
    except Exception as e:
        print(e)
        return render_template("webhook.html", \
        checked_settings=webhook_checked_settings, server_name=webhook_server_name, \
        server_url=webhook_server_url, shared_secret=webhook_shared_secret, \
        default_destination=webhook_default_destination)   

