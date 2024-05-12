import psutil

# Function to get CPU load
def get_cpu_load():
    return psutil.cpu_percent(interval=1, percpu=True)

# Function to get RAM usage
def get_ram_usage():
    return psutil.virtual_memory().percent

# Function to get disk usage
def get_disk_usage():
    return psutil.disk_usage('/').percent

# Function to get network usage
def get_network_usage():
    # For simplicity, this example assumes only one network interface
    return psutil.net_io_counters().bytes_sent, psutil.net_io_counters().bytes_recv

# Function to generate the output
def generate_output():
    cpu_load = get_cpu_load()
    ram_usage = get_ram_usage()
    disk_usage = get_disk_usage()
    network_usage = get_network_usage()

    output = f"Object          Metric                                   Values\n"
    output += f"--------------- ---------------------------------------- --------------------------------------------\n"
    output += f"host            CPU/Load/User                            {cpu_load[0]}%\n"
    output += f"host            CPU/Load/Kernel                          {cpu_load[1]}%\n"
    output += f"host            CPU/Load/Idle                            {cpu_load[2]}%\n"
    output += f"host            RAM/Usage/Used                           {ram_usage}%\n"
    output += f"host            Disk/Usage/Used                          {disk_usage}%\n"
    output += f"host            Net/Rate/Rx                              {network_usage[1]} B/s\n"
    output += f"host            Net/Rate/Tx                              {network_usage[0]} B/s\n"

    return output

# Example usage
if __name__ == "__main__":
    print(generate_output())
