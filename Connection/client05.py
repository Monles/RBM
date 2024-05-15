import psutil
import socket
import json
import time

SERVER_IP = 'your_ubuntu_vm_ip'
SERVER_PORT = 12345
INTERVAL = 15  # reporting interval in seconds

def collect_stats():
    stats = {}
    # CPU usage
    stats['cpu'] = psutil.cpu_percent(interval=1)
    # RAM usage
    mem = psutil.virtual_memory()
    stats['ram'] = {
        'total': mem.total,
        'used': mem.used,
        'free': mem.free,
        'percent': mem.percent
    }
    # Network connections
    stats['network'] = []
    for conn in psutil.net_connections():
        conn_info = {
            'fd': conn.fd,
            'family': conn.family,
            'type': conn.type,
            'laddr': conn.laddr,
            'raddr': conn.raddr,
            'status': conn.status,
            'pid': conn.pid
        }
        stats['network'].append(conn_info)
    # System processes
    stats['processes'] = []
    for proc in psutil.process_iter(['pid', 'name', 'username', 'cpu_percent', 'memory_info']):
        proc_info = proc.info
        stats['processes'].append(proc_info)
    return stats

def send_stats(stats):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((SERVER_IP, SERVER_PORT))
        s.sendall(json.dumps(stats).encode('utf-8'))

if __name__ == "__main__":
    while True:
        stats = collect_stats()
        send_stats(stats)
        time.sleep(INTERVAL - 1)  # Adjust sleep time to account for time spent collecting stats
