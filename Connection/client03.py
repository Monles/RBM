import psutil
import json
import time
import requests
from datetime import datetime

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

def print_data(data):
    print("CPU Usage:")
    for i, cpu in enumerate(data['cpu_percent']):
        print(f"CPU {i+1}: {cpu}%")
    
    print("\nMemory Usage:")
    print(f"Total: {data['mem_total']} bytes")
    print(f"Used: {data['mem_used']} bytes")
    print(f"Free: {data['mem_free']} bytes")
    
    print("\nNetwork Connections:")
    for conn in data['net_connections']:
        print(f"Local Address: {conn.laddr}, Remote Address: {conn.raddr}, Status: {conn.status}")
    
    print("\nSystem Processes:")
    for process in data['processes']:
        print(f"PID: {process['pid']}, Name: {process['name']}, CPU Percent: {process['cpu_percent']}%, Memory Percent: {process['memory_percent']}%")

def save_data_to_file(data, timestamp):
    filename = f"{timestamp}.data"
    with open(filename, 'w') as file:
        json.dump(data, file)
    print(f"Data saved to file: {filename}")

def send_data_to_server(data):
    server_url = 'http://ubuntu_vm_ip_address:5000/receive_data'
    try:
        response = requests.post(server_url, json=data)
        if response.status_code == 200:
            print("Data sent to server successfully!")
        else:
            print(f"Failed to send data to server. Status code: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"Error sending data to server: {e}")

if __name__ == "__main__":
    while True:
        timestamp = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
        data = collect_data()
        save_data_to_file(data, timestamp)
        send_data_to_server(data)
        time.sleep(15)  # Send data every 15 seconds
