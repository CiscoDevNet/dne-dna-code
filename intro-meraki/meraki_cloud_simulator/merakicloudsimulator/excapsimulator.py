"""Cisco Meraki Cloud Simulator for External Captive Portal labs."""
from merakicloudsimulator import merakicloudsimulator
from flask import request, render_template, redirect, jsonify, abort
import random
import requests
from datetime import datetime

# Module Variables
captive_portal_url = ""
user_continue_url = ""
window = ""
splash_logins = []

# Helper Functions
def generate_fake_mac():
    """Generate a fake MAC address."""
    hex_characters = "0123456789abcdef"

    def random_byte():
        """Generate a random byte."""
        return random.choice(hex_characters) + random.choice(hex_characters)

    return ":".join(random_byte() for _ in range(6))


# Flask micro-webservice API/URI endpoints
@merakicloudsimulator.route("/networks/<network_id>/ssids/<ssid_id>", methods=["PUT"])
def put_ssid(network_id, ssid_id):
    """Simulate setting SSID configurations."""
    print(f"Settings updated for network {network_id} ssid {ssid_id}.")
    return jsonify(request.json)


@merakicloudsimulator.route(
    "/networks/<network_id>/ssids/<ssid_id>/splashSettings",
    methods=["PUT"],
)
def put_splash(network_id, ssid_id):
    """Simulate setting Splash Page configurations."""
    print(f"Splash settings updated for network {network_id} ssid {ssid_id}.")
    return jsonify(request.json)


@merakicloudsimulator.route("/networks/<network_id>/splashLoginAttempts", methods=["GET"])
def get_splash_logins(network_id):
    """Get list of Splash Page logins."""
    # We aren't associating specific logins with a network ID
    _ = network_id
    return jsonify(splash_logins)


@merakicloudsimulator.route("/excap", methods=["GET"])
def excap_go():
    """Process GET requests to the /excap URI; render the index.html page."""
    return render_template("excap.html")


@merakicloudsimulator.route("/connecttowifi", methods=["POST"])
def connect_to_wifi():
    """Save captive portal details; redirect to the External Captive Portal."""

    captive_portal_url = request.form["captive_portal_url"]
    base_grant_url = request.host_url + "splash/grant"
    user_continue_url = request.form["user_continue_url"]
    node_mac = generate_fake_mac()
    client_ip = request.remote_addr
    client_mac = generate_fake_mac()
    splash_click_time = datetime.utcnow().isoformat()
    full_url = (
        captive_portal_url
        + "?base_grant_url=" + base_grant_url
        + "&user_continue_url=" + user_continue_url
        + "&node_mac=" + node_mac
        + "&client_ip=" + client_ip
        + "&client_mac=" + client_mac
    )

    splash_logins.append(
        {
            "name": "Simulated Client",
            "login": "simulatedclient@meraki.com",
            "ssid": "Simulated SSID",
            "loginAt": splash_click_time,
            "gatewayDeviceMac": node_mac,
            "clientMac": client_mac,
            "clientId": client_ip,
            "authorization": "success",
        }
    )

    return redirect(full_url, code=302)


@merakicloudsimulator.route("/splash/grant", methods=["GET"])
def continue_to_url():
    """Accept captive portal click-through; redirect to the continue URL."""
    return redirect(request.args.get("continue_url"), code=302)
