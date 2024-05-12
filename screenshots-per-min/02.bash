#!/bin/bash

# Replace '/path/to/screenshots' with the directory where you want to save the screenshots
screenshots_dir="/path/to/screenshots"

# Use vmrun command to capture screenshots of virtual machines
# Example: vmrun -T ws captureScreenshot /path/to/virtual_machine.vmx /path/to/save/screenshot.png

# Replace '/path/to/virtual_machine.vmx' with the actual path to the virtual machine configuration file
# Replace '/path/to/save/screenshot.png' with the path where you want to save the screenshot
# Repeat the vmrun command for each virtual machine you want to capture screenshots from

vmrun -T ws captureScreenshot /path/to/virtual_machine1.vmx "$screenshots_dir/screenshot_vm1.png"
vmrun -T ws captureScreenshot /path/to/virtual_machine2.vmx "$screenshots_dir/screenshot_vm2.png"
# Add more commands as needed for additional virtual machines

# Optionally, you can add a timestamp to each screenshot filename
# timestamp=$(date +"%Y-%m-%d_%H-%M-%S")
# vmrun -T ws captureScreenshot /path/to/virtual_machine.vmx "$screenshots_dir/screenshot_vm1_$timestamp.png"
