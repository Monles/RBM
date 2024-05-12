import psutil

def get_cpu_metrics():
    cpu_percent = psutil.cpu_percent(interval=1, percpu=True)
    return {'CPU/Load/User': cpu_percent[0], 'CPU/Load/Kernel': cpu_percent[2], 'CPU/Load/Idle': cpu_percent[3]}

def get_memory_metrics():
    virtual_memory = psutil.virtual_memory()
    return {'RAM/Usage/Total': virtual_memory.total, 'RAM/Usage/Used': virtual_memory.used, 'RAM/Usage/Free': virtual_memory.free}

def get_disk_metrics():
    disk_usage = psutil.disk_usage('/')
    return {'Disk/Usage/Total': disk_usage.total, 'Disk/Usage/Used': disk_usage.used}

def get_network_metrics():
    net_io_counters = psutil.net_io_counters()
    return {'Net/Rate/Rx': net_io_counters.bytes_recv, 'Net/Rate/Tx': net_io_counters.bytes_sent}

def generate_output():
    metrics = {
        'host': {
            **get_cpu_metrics(),
            **get_memory_metrics(),
            **get_disk_metrics(),
            **get_network_metrics()
        }
    }
    output = ''
    for object_name, metrics_dict in metrics.items():
        output += f"{object_name:<15} {'Metric':<40} {'Values':<50}\n"
        output += '-' * 95 + '\n'
        for metric, value in metrics_dict.items():
            output += f"{object_name:<15} {metric:<40} {str(value):<50}\n"
    return output

print(generate_output())
