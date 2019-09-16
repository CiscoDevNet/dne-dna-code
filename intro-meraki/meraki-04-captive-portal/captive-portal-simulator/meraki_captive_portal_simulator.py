"""
Cisco Meraki Captive Portal simulator

Default port: 5003

Matt DeNapoli

2018

https://developer.cisco.com/site/Meraki
"""

# Libraries
from flask import Flask, request, render_template, redirect, url_for
import random
import datetime
import time
import requests
import webview
import netifaces as nif
import datetime
import threading

app = Flask(__name__)

# Globals
global captive_portal_url
captive_portal_url = ""
global user_continue_url
user_continue_url = ""
global window
window = ""


@app.route("/go", methods=["GET"])
def get_go():
    return render_template("index.html", **locals())

# Kick off simulator and create baseline dataset
@app.route("/connecttowifi", methods=["POST"])
def connect_to_wifi():
    global captive_portal_url
    global user_continue_url

    captive_portal_url = request.form["captive_portal_url"]
    base_grant_url = request.host_url + "splash/grant";
    user_continue_url = request.form["user_continue_url"]
    node_mac = generate_fake_mac()
    client_ip = request.remote_addr
    client_mac = generate_fake_mac()
    splashclick_time = datetime.datetime.now()
    full_url = captive_portal_url + \
    "?base_grant_url=" + base_grant_url + \
    "&user_continue_url=" + user_continue_url + \
    "&node_mac=" + node_mac + \
    "&client_ip=" + client_ip + \
    "&client_mac=" + client_mac
    window.load_url(full_url)

    return render_template("connected.html", full_url=full_url)

@app.route("/splash/grant", methods=["GET"])
def continue_to_url():
    return redirect(request.args.get("continue_url"), code=302)

def generate_fake_mac():
    fake_mac = ""
    for mac_part in range(6):
        fake_mac += "".join(
            random.choice("0123456789abcdef") for i in range(2)
        )
        if mac_part < 5:
            fake_mac += ":"

    return fake_mac

@app.route("/setupserver", methods=["GET"])
def setupserver():
    return render_template("setupserver.html", serversetupurl=request.host_url
    + "go")

def start_server():
    app.run(host="0.0.0.0", threaded=True, port=5003, debug=False)

if __name__ == "__main__":
    t = threading.Thread(target = start_server)
    t.dameon = True
    t.start()

    window = webview.create_window("Captive Portal", "http://localhost:5003/setupserver",
    js_api=None, width=800, height=600, resizable=True, fullscreen=False,
    min_size=(200, 100), confirm_close=False,
    background_color='#FFF', text_select=True)
    webview.start()