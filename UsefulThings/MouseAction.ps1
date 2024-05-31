# Add necessary types for user input simulation
Add-Type @"
using System;
using System.Runtime.InteropServices;

public class UserInput {
    [DllImport("user32.dll", CharSet = CharSet.Auto, CallingConvention = CallingConvention.StdCall)]
    public static extern void mouse_event(uint dwFlags, uint dx, uint dy, uint cButtons, uint dwExtraInfo);

    [DllImport("user32.dll")]
    public static extern uint keybd_event(byte bVk, byte bScan, uint dwFlags, uint dwExtraInfo);
}
"@

# Constants for mouse events
$MOUSEEVENTF_MOVE = 0x0001
$MOUSEEVENTF_ABSOLUTE = 0x8000
$MOUSEEVENTF_LEFTDOWN = 0x0002
$MOUSEEVENTF_LEFTUP = 0x0004

# Function to move the mouse to a specific position
function Move-Mouse {
    param (
        [int]$x,
        [int]$y
    )
    [UserInput]::mouse_event($MOUSEEVENTF_MOVE -bor $MOUSEEVENTF_ABSOLUTE, $x * 65535 / [System.Windows.Forms.SystemInformation]::PrimaryMonitorSize.Width, $y * 65535 / [System.Windows.Forms.SystemInformation]::PrimaryMonitorSize.Height, 0, 0)
}

# Function to click the mouse
function Click-Mouse {
    [UserInput]::mouse_event($MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)
    Start-Sleep -Milliseconds 100
    [UserInput]::mouse_event($MOUSEEVENTF_LEFTUP, 0, 0, 0, 0)
}

# Function to type text
function Type-Text {
    param (
        [string]$text
    )
    foreach ($char in $text.ToCharArray()) {
        $keyCode = [byte][char]$char
        [UserInput]::keybd_event($keyCode, 0, 0, 0)
        Start-Sleep -Milliseconds 100
        [UserInput]::keybd_event($keyCode, 0, 2, 0)
    }
}

# Move the mouse to the bottom left corner and click (to ensure focus is reset)
Move-Mouse -x 10 -y 1080
Click-Mouse

# Move the mouse to the start menu and click
Move-Mouse -x 50 -y 1060
Click-Mouse
Start-Sleep -Seconds 1

# Type 'notepad' to open Notepad
Type-Text -text "notepad"
Start-Sleep -Milliseconds 500

# Press Enter to open Notepad
[UserInput]::keybd_event(0x0D, 0, 0, 0)
Start-Sleep -Milliseconds 100
[UserInput]::keybd_event(0x0D, 0, 2, 0)

Start-Sleep -Seconds 2

# Type some text into Notepad
Type-Text -text "Hello, this is a test message."

# Save the file
[UserInput]::keybd_event(0x11, 0, 0, 0) # Ctrl
[UserInput]::keybd_event(0x53, 0, 0, 0) # S
Start-Sleep -Milliseconds 100
[UserInput]::keybd_event(0x53, 0, 2, 0) # S Up
[UserInput]::keybd_event(0x11, 0, 2, 0) # Ctrl Up

Start-Sleep -Seconds 1

# Type the file name
Type-Text -text "C:\Temp\TestFile.txt"
Start-Sleep -Milliseconds 500

# Press Enter to save the file
[UserInput]::keybd_event(0x0D, 0, 0, 0)
Start-Sleep -Milliseconds 100
[UserInput]::keybd_event(0x0D, 0, 2, 0)

Start-Sleep -Seconds 1

# Close Notepad
[UserInput]::keybd_event(0x12, 0, 0, 0) # Alt
[UserInput]::keybd_event(0x73, 0, 0, 0) # F4
Start-Sleep -Milliseconds 100
[UserInput]::keybd_event(0x73, 0, 2, 0) # F4 Up
[UserInput]::keybd_event(0x12, 0, 2, 0) # Alt Up
