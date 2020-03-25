"""Cisco Meraki Cloud Simulator for External Captive Portal labs."""

from merakicloudsimulator import merakicloudsimulator
from merakicloudsimulator.meraki_settings import ORGANIZATIONS, NETWORKS
from flask import render_template,jsonify,abort

# Module Constants & Simulated Cloud Data
WEB_SERVER_HOSTNAME = "localhost"
WEB_SERVER_BIND_IP = "0.0.0.0"
WEB_SERVER_BIND_PORT = 5001

@merakicloudsimulator.route("/go", methods=["GET"])
def meraki_simulator_go():
    return render_template("index.html")

# Flask micro-webservice API/URI endpoints
@merakicloudsimulator.route("/organizations", methods=["GET"])
def get_org_id():
    """Get a list of simulated organizations."""
    return jsonify(ORGANIZATIONS)


@merakicloudsimulator.route("/organizations/<organization_id>/networks", methods=["GET"])
def get_networks(organization_id):
    """Get the list of networks for an organization."""
    organization_networks = NETWORKS.get(organization_id)
    if organization_networks:
        return jsonify(organization_networks)
    else:
        abort(404)

if __name__ == "__main__":
    print(
        f"\n>>> "
        f"Open your browser and browse to "
        f"http://{WEB_SERVER_HOSTNAME}:{WEB_SERVER_BIND_PORT}/go "
        f"to configure the captive portal and simulate a client login."
        f" <<<\n"
    )

    # Start the web server
    merakicloudsimulator.run(host=WEB_SERVER_BIND_IP, port=WEB_SERVER_BIND_PORT, threaded=True, debug=False)