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
        "memory": [
            virtual_memory.total, virtual_memory.available,
            virtual_memory.percent, virtual_memory.used, virtual_memory.free
        ],
        "swap": [
            swap_memory.total, swap_memory.used, swap_memory.free,
            swap_memory.percent, swap_memory.sin, swap_memory.sout
        ]
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
                net_io_counters[nic].bytes_sent,
                net_io_counters[nic].bytes_recv,
                net_io_counters[nic].packets_sent,
                net_io_counters[nic].packets_recv, net_io_counters[nic].errin,
                net_io_counters[nic].errout, net_io_counters[nic].dropin,
                net_io_counters[nic].dropout
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
        net_conns.append([
            conn.fd, conn.family, conn.type, [conn.laddr.ip, conn.laddr.port],
            [conn.raddr.ip, conn.raddr.port] if conn.raddr else [],
            conn.status, conn.pid
        ])
    return net_conns


def get_disk_io_counters():
    disk_io = psutil.disk_io_counters(perdisk=True)
    disk_io_counters = {
        disk: [
            io.read_count, io.write_count, io.read_bytes, io.write_bytes,
            io.read_time, io.write_time
        ]
        for disk, io in disk_io.items()
    }
    return disk_io_counters


def capture_screenshot():
    # Capture the screenshot
    im = ImageGrab.grab()
    # Get the current datetime for the filename
    dt = datetime.now()
    fname = "pic_{}.{}.png".format(dt.strftime("%Y%m%d_%H%M_%S"),
                                   dt.microsecond // 100000)
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
            print(
                f"Failed to send screenshot. Status code: {response.status_code}"
            )


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


def collect_cpu_metrics(metrics):
    cpu_times = psutil.cpu_times_percent(interval=1)
    cpu_freq = psutil.cpu_freq()
    metrics["host CPU/Load/User"] = f"{cpu_times.user}%"
    metrics["host CPU/Load/User:avg"] = f"{cpu_times.user}%"
    metrics["host CPU/Load/User:min"] = f"{cpu_times.user}%"
    metrics["host CPU/Load/User:max"] = f"{cpu_times.user}%"
    metrics["host CPU/Load/Kernel"] = f"{cpu_times.system}%"
    metrics["host CPU/Load/Kernel:avg"] = f"{cpu_times.system}%"
    metrics["host CPU/Load/Kernel:min"] = f"{cpu_times.system}%"
    metrics["host CPU/Load/Kernel:max"] = f"{cpu_times.system}%"
    metrics["host CPU/Load/Idle"] = f"{cpu_times.idle}%"
    metrics["host CPU/Load/Idle:avg"] = f"{cpu_times.idle}%"
    metrics["host CPU/Load/Idle:min"] = f"{cpu_times.idle}%"
    metrics["host CPU/Load/Idle:max"] = f"{cpu_times.idle}%"
    metrics["host CPU/MHz"] = f"{cpu_freq.current} MHz"
    metrics["host CPU/MHz:avg"] = f"{cpu_freq.current} MHz"
    metrics["host CPU/MHz:min"] = f"{cpu_freq.min} MHz"
    metrics["host CPU/MHz:max"] = f"{cpu_freq.max} MHz"


def enumerate_ram_metrics():
    virtual_memory = psutil.virtual_memory()
    ram_metrics = {}
    for attr in dir(virtual_memory):
        if not attr.startswith('_') and not callable(
                getattr(virtual_memory, attr)):
            value = getattr(virtual_memory, attr)
            ram_metrics[attr] = value
    return ram_metrics


def collect_ram_metrics(metrics):
    virtual_memory = psutil.virtual_memory()
    metrics["host RAM/Usage/Total"] = f"{virtual_memory.total // 1024} kB"
    metrics["host RAM/Usage/Total:avg"] = f"{virtual_memory.total // 1024} kB"
    metrics["host RAM/Usage/Total:min"] = f"{virtual_memory.total // 1024} kB"
    metrics["host RAM/Usage/Total:max"] = f"{virtual_memory.total // 1024} kB"
    metrics["host RAM/Usage/Used"] = f"{virtual_memory.used // 1024} kB"
    metrics["host RAM/Usage/Used:avg"] = f"{virtual_memory.used // 1024} kB"
    metrics["host RAM/Usage/Used:min"] = f"{virtual_memory.used // 1024} kB"
    metrics["host RAM/Usage/Used:max"] = f"{virtual_memory.used // 1024} kB"
    metrics["host RAM/Usage/Free"] = f"{virtual_memory.available // 1024} kB"
    metrics[
        "host RAM/Usage/Free:avg"] = f"{virtual_memory.available // 1024} kB"
    metrics[
        "host RAM/Usage/Free:min"] = f"{virtual_memory.available // 1024} kB"
    metrics[
        "host RAM/Usage/Free:max"] = f"{virtual_memory.available // 1024} kB"

    # Dynamically add other RAM metrics
    ram_metrics = enumerate_ram_metrics()
    for key, value in ram_metrics.items():
        if key not in metrics:  # Avoid overwriting the specifically requested metrics
            metrics[f"host RAM/{key}"] = f"{value // 1024} kB" if isinstance(
                value, int) else f"{value}"


def collect_network_metrics(metrics):
    net_io = psutil.net_io_counters(pernic=True)
    net_if_stats = psutil.net_if_stats()

    for interface, stats in net_io.items():
        if interface in net_if_stats:
            speed = f"{net_if_stats[interface].speed} Mb/s" if net_if_stats[
                interface].isup else "N/A"
        else:
            speed = "N/A"

        metrics[f"host Net/{interface}/LinkSpeed"] = speed
        metrics[f"host Net/{interface}/LinkSpeed:avg"] = speed
        metrics[f"host Net/{interface}/LinkSpeed:min"] = speed
        metrics[f"host Net/{interface}/LinkSpeed:max"] = speed
        metrics[f"host Net/{interface}/Load/Rx"] = f"{stats.bytes_recv} B"
        metrics[f"host Net/{interface}/Load/Rx:avg"] = f"{stats.bytes_recv} B"
        metrics[f"host Net/{interface}/Load/Rx:min"] = f"{stats.bytes_recv} B"
        metrics[f"host Net/{interface}/Load/Rx:max"] = f"{stats.bytes_recv} B"
        metrics[f"host Net/{interface}/Load/Tx"] = f"{stats.bytes_sent} B"
        metrics[f"host Net/{interface}/Load/Tx:avg"] = f"{stats.bytes_sent} B"
        metrics[f"host Net/{interface}/Load/Tx:min"] = f"{stats.bytes_sent} B"
        metrics[f"host Net/{interface}/Load/Tx:max"] = f"{stats.bytes_sent} B"


def collect_fs_metrics(metrics):
    disk_usage = psutil.disk_usage('/')
    metrics["host FS/{/}/Usage/Total"] = f"{disk_usage.total // 1024} kB"
    metrics["host FS/{/}/Usage/Total:avg"] = f"{disk_usage.total // 1024} kB"
    metrics["host FS/{/}/Usage/Total:min"] = f"{disk_usage.total // 1024} kB"
    metrics["host FS/{/}/Usage/Total:max"] = f"{disk_usage.total // 1024} kB"
    metrics["host FS/{/}/Usage/Used"] = f"{disk_usage.used // 1024} kB"
    metrics["host FS/{/}/Usage/Used:avg"] = f"{disk_usage.used // 1024} kB"
    metrics["host FS/{/}/Usage/Used:min"] = f"{disk_usage.used // 1024} kB"
    metrics["host FS/{/}/Usage/Used:max"] = f"{disk_usage.used // 1024} kB"
    metrics["host FS/{/}/Usage/Free"] = f"{disk_usage.free // 1024} kB"
    metrics["host FS/{/}/Usage/Free:avg"] = f"{disk_usage.free // 1024} kB"
    metrics["host FS/{/}/Usage/Free:min"] = f"{disk_usage.free // 1024} kB"
    metrics["host FS/{/}/Usage/Free:max"] = f"{disk_usage.free // 1024} kB"


def collect_system_metrics():
    metrics = {}

    collect_cpu_metrics(metrics)
    collect_ram_metrics(metrics)
    collect_network_metrics(metrics)
    collect_fs_metrics(metrics)

    return metrics


def save_metrics_to_file(metrics):
    timestamp = datetime.now().strftime("%d-%m-%Y-%H-%M-%S")
    filename = f"metrics_{timestamp}.data"
    with open(filename, "w") as file:
        for metric, value in metrics.items():
            file.write(f"{metric:<40} {value}\n")
    print(f"Metrics saved to {filename}")
    return filename


def send_file(server_url, filepath):
    with open(filepath, 'rb') as f:
        files = {'file': f}
        response = requests.post(server_url, files=files)
        if response.status_code == 200:
            print(f"File {filepath} sent successfully!")
        else:
            print(
                f"Failed to send file {filepath}. Status code: {response.status_code}"
            )


if __name__ == "__main__":
    server_url_data = "http://192.168.163.130:5000/receive_data"
    server_url_screenshot = "http://192.168.163.130:5000/receive_screenshot"
    server_url_file = "http://192.168.163.130:5000/receive_file"

    # Capture and send a screenshot right away
    screenshot_path = capture_screenshot()
    send_screenshot(server_url_screenshot, screenshot_path)

    last_screenshot_time = time.time()

    while True:
        # Collect and send system data
        data = collect_data()
        timestamp = datetime.now().strftime("%m-%d-%Y %H:%M:%S.%f")
        data['timestamp'] = timestamp
        headers = {'Content-Type': 'application/json'}
        response = requests.post(server_url_data, json=data, headers=headers)
        if response.status_code == 200:
            print("Data sent successfully!")
        else:
            print(f"Failed to send data. Status code: {response.status_code}")

        # Collect and send metrics to a file
        metrics = collect_system_metrics()
        metrics_file = save_metrics_to_file(metrics)
        send_file(server_url_file, metrics_file)

        # Check if it's time to take and send a screenshot
        current_time = time.time()
        if current_time - last_screenshot_time >= 60:
            screenshot_path = capture_screenshot()
            send_screenshot(server_url_screenshot, screenshot_path)
            last_screenshot_time = current_time

        time.sleep(15)  # Send data every 15 seconds
