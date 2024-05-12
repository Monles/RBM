import psutil

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

if __name__ == "__main__":
    data = collect_data()
    print_data(data)
