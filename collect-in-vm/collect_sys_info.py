import psutil

# Function to get system metrics
def get_system_metrics():
    metrics = []

    # CPU Metrics
    cpu_percent = psutil.cpu_percent(interval=1, percpu=True)
    for i, cpu in enumerate(cpu_percent):
        metrics.append(f"host            CPU/Load/User{i}                            {cpu}%")
        metrics.append(f"host            CPU/Load/User{i}:avg                        {cpu}%")
        metrics.append(f"host            CPU/Load/User{i}:min                        {cpu}%")
        metrics.append(f"host            CPU/Load/User{i}:max                        {cpu}%")

    # Memory Metrics
    mem = psutil.virtual_memory()
    metrics.append(f"host            RAM/Usage/Total                          {mem.total} B")
    metrics.append(f"host            RAM/Usage/Used                           {mem.used} B")
    metrics.append(f"host            RAM/Usage/Free                           {mem.free} B")

    # Disk Metrics
    disk_usage = psutil.disk_usage('/')
    metrics.append(f"host            Disk/Usage/Total                         {disk_usage.total} B")
    metrics.append(f"host            Disk/Usage/Used                          {disk_usage.used} B")
    metrics.append(f"host            Disk/Usage/Free                          {disk_usage.free} B")

    # Network Metrics
    net_io_counters = psutil.net_io_counters()
    metrics.append(f"host            Net/Rate/Rx                              {net_io_counters.bytes_recv} B/s")
    metrics.append(f"host            Net/Rate/Tx                              {net_io_counters.bytes_sent} B/s")

    return metrics

# Main function to generate the output
def generate_output(metrics):
    output = "Object          Metric                                   Values\n--------------- ---------------------------------------- --------------------------------------------\n"
    for metric in metrics:
        output += metric + "\n"
    return output

# Get system metrics
metrics = get_system_metrics()

# Generate output
output = generate_output(metrics)

# Print or write to a file
print(output)
# This can also write it to a file
# with open("system_metrics.txt", "w") as file:
#     file.write(output)
