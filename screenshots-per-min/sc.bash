#!/bin/bash

# Array containing paths to VM configuration files
vm_configs=(
    "/path/to/vm1.vmx"
    "/path/to/vm2.vmx"
    "/path/to/vm3.vmx"
    # Add paths for more VMs as needed
)

# Loop through each VM
for vm_config in "${vm_configs[@]}"; do
    # Start the VM
    vmrun -T ws start "$vm_config" nogui

    # Capture a screenshot
    vmrun -T ws captureScreen "$vm_config" /path/to/save/screenshot-$(date +%Y%m%d%H%M%S).png

    # Stop the VM
    vmrun -T ws stop "$vm_config" soft
done
