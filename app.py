from flask import Flask, request, jsonify
import subprocess

# Initialize Flask application
app = Flask(__name__)

# Define network interface name
INTERNAL_IFACE = "wlan0"

def run_cmd(cmd):
    """
    Function to run a shell command and return its output.
    If the command fails, it returns None.

    Parameters:
    cmd (str): The shell command to run.

    Returns:
    str: The output of the command, or None if the command fails.
    """
    try:
        result = subprocess.run(cmd, shell=True, check=True, stdout=subprocess.PIPE, universal_newlines=True)
        return result.stdout
    except subprocess.CalledProcessError:
        return None

@app.route('/wifi')
def wifi():
    """
    Endpoint to list all available Wi-Fi networks.

    Returns:
    JSON: A list of dictionaries, each containing the SSID and signal strength of a network.
    """
    cmd = f"nmcli --colors no -f SSID,BARS dev wifi list ifname {INTERNAL_IFACE}"
    output = run_cmd(cmd)
    if output:
        wifi_list = [{'ssid': ssid, 'bars': bars} for ssid, bars in (line.split() for line in output.splitlines()[1:])]
        return jsonify(wifi_list)
    return jsonify({'success': False, 'error': 'Failed to get wifi list'}), 500

@app.route('/wifi/current')
def wifi_current():
    """
    Endpoint to get the SSID of the currently connected Wi-Fi network.

    Returns:
    JSON: A dictionary containing the SSID of the current network.
    """
    cmd = f"nmcli -t -f active,ssid dev wifi list ifname {INTERNAL_IFACE}"
    output = run_cmd(cmd)
    if output and ':' in output:
        ssid = output.split(':')[1].strip()
        return jsonify({'ssid': ssid})
    return jsonify({'success': False, 'error': 'Failed to get current wifi'}), 500

@app.route('/wifi/connect', methods=['POST'])
def wifi_connect():
    """
    Endpoint to connect to a Wi-Fi network.
    Takes a JSON payload containing the SSID and password of the network.

    Returns:
    JSON: A dictionary indicating whether the connection was successful.
    """
    ssid = request.json.get('ssid')
    password = request.json.get('password')
    if ssid and password:
        cmd = f"nmcli dev wifi connect {ssid} password {password} ifname {INTERNAL_IFACE}"
        if run_cmd(cmd):
            return jsonify({'success': True})
    return jsonify({'success': False, 'error': 'Failed to connect to wifi'}), 500

@app.route('/vpn/status')
def vpn_status():
    """
    Endpoint to get the current status of the VPN connection.

    Returns:
    JSON: A dictionary containing the status of the VPN connection.

    Sample Response:
    {
        "Status": "Connected",
        "Hostname": "xxxx.nordvpn.com",
        "IP": "x.x.x.x",
        "Country": "Canada",
        "City": "Montreal",
        "Current technology": "NORDLYNX",
        "Current protocol": "UDP",
        "Transfer": "14.30 MiB received, 1.99 MiB sent",
        "Uptime": "8 minutes 52 seconds"
    }
    """
    cmd = "nordvpn status"
    output = run_cmd(cmd)
    if output:
        status = {key: value.strip() for key, value in (line.split(':') for line in output.splitlines())}
        return jsonify(status)
    return jsonify({'success': False, 'error': 'Failed to get VPN status'}), 500

@app.route('/vpn/connect', methods=['POST'])
def vpn_connect():
    """
    Endpoint to connect to a VPN server.
    Takes a JSON payload containing the city of the server.

    Returns:
    JSON: A dictionary indicating whether the connection was successful.
    """
    city = request.json.get('city')
    if city:
        cmd = f"nordvpn connect {city}"
        if run_cmd(cmd):
            return jsonify({'success': True})
    return jsonify({'success': False, 'error': 'Failed to connect to VPN'}), 500

@app.route('/vpn/disconnect')
def vpn_disconnect():
    cmd = "nordvpn disconnect"
    if run_cmd(cmd):
        return jsonify({'success': True})
    return jsonify({'success': False, 'error': 'Failed to disconnect from VPN'}), 500