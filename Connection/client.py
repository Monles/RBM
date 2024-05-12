import psutil
import requests
import json

def collect_system_data():
    # Collect system data
    data = {
        "cpu_percent": psutil.cpu_percent(),
        "ram_percent": psutil.virtual_memory().percent,
        # Add more data points as needed
    }
    return data

def send_data_to_server(data):
    url = 'http://<ubuntu_vm_ip>:<port>/receive_data'
    headers = {'Content-type': 'application/json'}
    response = requests.post(url, headers=headers, data=json.dumps(data))
    if response.status_code == 200:
        print("Data sent successfully to Ubuntu server.")
    else:
        print("Failed to send data to Ubuntu server.")

if __name__ == "__main__":
    system_data = collect_system_data()
    send_data_to_server(system_data)
