import json
import psutil
import requests

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
    # Convert net_connections to a list of dictionaries for JSON serialization
    net_connections_list = [{'laddr': conn.laddr, 'raddr': conn.raddr, 'status': conn.status} for conn in net_connections]
    data['net_connections'] = net_connections_list
    
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
    # Collect data
    data = collect_data()
    
    # Send data to the Ubuntu VM
    ubuntu_vm_ip = 'ubuntu_vm_ip_address'  # Replace with the IP address of your Ubuntu VM
    url = f'http://{ubuntu_vm_ip}:5000/receive_data'  # Assuming the Flask endpoint is '/receive_data'
    
    # Convert data to JSON
    json_data = json.dumps(data)
    
    # Send POST request
    response = requests.post(url, json=json_data)
    
    # Print response from the server
    print(response.text)
