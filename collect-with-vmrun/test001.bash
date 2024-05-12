# Start the virtual machine
vmrun -T ws start "/path/to/virtual_machine.vmx" nogui

# Execute commands inside the virtual machine to gather information
# For example, to collect CPU usage information:
vmrun -T ws -gu guest_username -gp guest_password runProgramInGuest "/path/to/virtual_machine.vmx" "/bin/bash" "-c" "top -bn1 > cpu_usage.txt"

# Similarly, gather RAM and HDD usage information
vmrun -T ws -gu guest_username -gp guest_password runProgramInGuest "/path/to/virtual_machine.vmx" "/bin/bash" "-c" "free -m > ram_usage.txt"
vmrun -T ws -gu guest_username -gp guest_password runProgramInGuest "/path/to/virtual_machine.vmx" "/bin/bash" "-c" "df -h > hdd_usage.txt"

# Stop the virtual machine
vmrun -T ws stop "/path/to/virtual_machine.vmx" soft
