from pprint import pprint
from flask import Flask, request, render_template, redirect, url_for, json
import sys, getopt
import json

app = Flask(__name__)

global base_grant_url
base_grant_url = ""
global user_continue_url
user_continue_url = ""
global success_url
success_url = ""

@app.route("/click", methods=["GET"])
def get_click():
    global base_grant_url
    global user_continue_url
    global success_url

    host = request.host_url
    base_grant_url = request.args.get('base_grant_url')
    user_continue_url = request.args.get('user_continue_url')
    node_mac = request.args.get('node_mac')
    client_ip = request.args.get('client_ip')
    client_mac = request.args.get('client_mac ')
    splashclick_time = request.args.get('splashclick_time')
    success_url = host + "success"

    return render_template("click.html", client_ip=client_ip,
    client_mac=client_mac, node_mac=node_mac,
    user_continue_url=user_continue_url,success_url=success_url)


@app.route("/login", methods=["POST"])
def get_login():
    global base_grant_url
    global success_url

    user_email = request.form["user_email_address"]

    return redirect(base_grant_url+"?continue_url="+success_url, code=302)

@app.route("/success",methods=["GET"])
def get_success():
    global user_continue_url

    return render_template("success.html",user_continue_url=user_continue_url)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5004, debug=False)
