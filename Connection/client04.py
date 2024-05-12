import psutil
import requests
import json
from datetime import datetime
import time

def collect_data():
    data = {}
    
    # CPU Usage
    cpu_percent = psutil.cpu_percent(interval=1, percpu=True)
    data['cpu_percent'] = cpu_percent
    
    # Memory Usage
    mem = psutil.virtual_memory()
    data['mem_total'] = mem.total
    data['mem_used'] = mem.used
    data['mem_free'] = mem.free
    
    # Network Connections
    net_connections = psutil.net_connections(kind='inet')
    data['net_connections'] = net_connections
    
    # System Processes
    processes = []
    for process in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent']):
        processes.append({
            'pid': process.info['pid'],
            'name': process.info['name'],
            'cpu_percent': process.info['cpu_percent'],
            'memory_percent': process.info['memory_percent']
        })
    data['processes'] = processes
    
    return data

if __name__ == "__main__":
    server_url = "http://<ubuntu_vm_ip>:5000/receive_data"
    while True:
        data = collect_data()
        timestamp = datetime.now().strftime("%m-%d-%Y-%H-%M-%S")
        data['timestamp'] = timestamp
        headers = {'Content-Type': 'application/json'}
        response = requests.post(server_url, json=data, headers=headers)
        if response.status_code == 200:
            print("Data sent successfully!")
        else:
            print(f"Failed to send data. Status code: {response.status_code}")
        time.sleep(15)  # Send data every 15 seconds
