import socket
import uuid
import platform
import urllib.request
import json
import time
import subprocess
 
SERVER_URL = "http://127.0.0.1:8000/api/register/"
COMMAND_URL = "http://127.0.0.1:8000/api/get-commands/"

def get_mac_address():
    mac = uuid.getnode()
    return ':'.join(('%012X' % mac)[i:i+2] for i in range(0, 12, 2))

def register_with_server():
    mac = get_mac_address()
    data = {
        "hostname": socket.gethostname(),
        "ip_address": socket.gethostbyname(socket.gethostname()),
        "mac_address": mac,
        "os_version": f"{platform.system()} {platform.release()}"
    }
    json_data = json.dumps(data).encode('utf-8')
    req = urllib.request.Request(SERVER_URL, data=json_data, headers={'Content-Type': 'application/json'})
    try:
        urllib.request.urlopen(req)
        print(f"Connected to Server! Agent running on {data['hostname']}")
        return mac
    except Exception as e:
        print("Waiting for server connection...")
        return None

def listen_for_commands(mac_address):
    url = f"{COMMAND_URL}{mac_address}/"
    while True:
        try:
            response = urllib.request.urlopen(url)
            result = json.loads(response.read().decode('utf-8'))
            
            if result.get('has_command'):
                cmd = result['command']
                print(f"\n[!] ALERT: Received command from server: {cmd}")
                print("Executing...")
                
                # Upgraded execution method for better Windows compatibility
                subprocess.run(cmd, shell=True, check=False)
                
        except Exception as e:
            pass # Fail silently and wait for next check
            
        time.sleep(5)

if __name__ == "__main__":
    mac = None
    while not mac:
        mac = register_with_server()
        if not mac:
            time.sleep(5)
            
    # Start the continuous listening loop
    listen_for_commands(mac)   
