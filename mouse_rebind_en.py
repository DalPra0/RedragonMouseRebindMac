#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import usb.core
import usb.util
import sys
import time

def decimal_to_hex(decimal_value):
    """Converts a decimal value to hexadecimal, properly formatted."""
    return f"0x{decimal_value:04X}"

def get_user_input(prompt, default=None, is_int=False):
    """Gets user input with optional default value."""
    if default is not None:
        prompt = f"{prompt} [{default}]: "
    else:
        prompt = f"{prompt}: "
        
    while True:
        user_input = input(prompt).strip()
        
        if not user_input and default is not None:
            return default
            
        if is_int:
            try:
                return int(user_input, 0)  # Accepts decimal (123) or hex (0x7B)
            except ValueError:
                print("Error: Please enter a valid number (decimal or hexadecimal).")
        else:
            return user_input

def send_command_to_mouse(vid, pid, payload, interface=0, report_type=0x0300):
    """
    Sends a control command to the mouse.
    
    Args:
        vid: Vendor ID of the device
        pid: Product ID of the device
        payload: List of bytes to send
        interface: Interface number (default 0)
        report_type: Report type (default 0x0300)
    
    Returns:
        bool: True if the command was sent successfully, False otherwise
    """
    try:
        # Find the device
        print(f"\nFinding device with VID={decimal_to_hex(vid)}, PID={decimal_to_hex(pid)}...")
        dev = usb.core.find(idVendor=vid, idProduct=pid)
        
        if dev is None:
            print(f"Error: Device with VID={decimal_to_hex(vid)}, PID={decimal_to_hex(pid)} not found!")
            return False
            
        print(f"Device found!")
        
        # Detach from kernel if necessary (Linux)
        try:
            for i in range(3):  # Try on multiple interfaces
                if dev.is_kernel_driver_active(i):
                    print(f"Releasing kernel driver on interface {i}...")
                    dev.detach_kernel_driver(i)
        except Exception as e:
            print(f"Warning while releasing driver: {e}")
        
        # Configure the device
        print("Configuring device...")
        try:
            dev.set_configuration()
        except Exception as e:
            print(f"Warning during configuration: {e}")
            print("Trying to continue anyway...")
        
        # Send the control command
        print(f"Sending command: {[hex(x) for x in payload]}")
        result = dev.ctrl_transfer(
            0x21,      # Request type (Class | Interface)
            0x09,      # SET_REPORT
            report_type,
            interface,
            payload,
            timeout=1000
        )
        
        print(f"Command sent successfully! Bytes transferred: {result}")
        return True
        
    except usb.core.USBError as e:
        print(f"USB error while sending command: {e}")
        return False
    except Exception as e:
        print(f"General error while sending command: {e}")
        return False

def get_payload_from_user():
    """Asks the user to enter the byte sequence for the payload."""
    print("\nEnter payload as a sequence of bytes (hexadecimal or decimal values).")
    print("For example: 0x01 0x00 0x04 or 1 0 4")
    
    payload_str = input("Payload: ")
    payload_parts = payload_str.split()
    
    payload = []
    for part in payload_parts:
        try:
            # Convert string to integer (decimal or hex)
            byte_value = int(part, 0)
            if 0 <= byte_value <= 255:
                payload.append(byte_value)
            else:
                print(f"Warning: Value {part} outside valid range for a byte (0-255), using 0.")
                payload.append(0)
        except ValueError:
            print(f"Warning: Invalid value '{part}', using 0 instead.")
            payload.append(0)
    
    if not payload:
        print("Empty payload, using default values [0x01, 0x00, 0x04]")
        return [0x01, 0x00, 0x04]
        
    return payload

def interactive_mode():
    """Interactive interface to configure and send commands to the mouse."""
    print("\n" + "=" * 60)
    print("USB MOUSE REBIND CONFIGURATION")
    print("=" * 60)
    
    print("\nThis script sends commands to configure your USB mouse.")
    print("If you don't know your mouse's VID/PID, run 'mouse_finder_en.py' first.")
    
    print("\n" + "-" * 60)
    print("DEVICE CONFIGURATION")
    print("-" * 60)
    
    # Get device information
    vid = get_user_input("Enter mouse VID (decimal or hex)", default=0x25A7, is_int=True)
    pid = get_user_input("Enter mouse PID (decimal or hex)", default=0xFA08, is_int=True)
    
    print(f"\nVID: {vid} ({decimal_to_hex(vid)})")
    print(f"PID: {pid} ({decimal_to_hex(pid)})")
    
    # Get advanced parameters
    interface = get_user_input("Enter interface number", default=0, is_int=True)
    
    report_type_default = 0x0300
    report_type = get_user_input(
        "Enter Report Type",
        default=f"0x{report_type_default:04X}",
        is_int=True
    )
    
    # Get payload
    payload = get_payload_from_user()
    
    # Confirmation
    print("\n" + "-" * 60)
    print("CONFIGURATION SUMMARY")
    print("-" * 60)
    print(f"VID: {vid} ({decimal_to_hex(vid)})")
    print(f"PID: {pid} ({decimal_to_hex(pid)})")
    print(f"Interface: {interface}")
    print(f"Report Type: {report_type} ({decimal_to_hex(report_type)})")
    print(f"Payload: {[hex(x) for x in payload]}")
    
    confirm = input("\nConfirm and send command? (y/n): ").strip().lower()
    if confirm != 'y':
        print("Operation cancelled by user.")
        return
    
    # Send the command
    if send_command_to_mouse(vid, pid, payload, interface, report_type):
        print("\nCommand processed successfully!")
    else:
        print("\nFailed to process command. Check the device and permissions.")

def main():
    try:
        interactive_mode()
    except KeyboardInterrupt:
        print("\n\nOperation interrupted by user.")
    except Exception as e:
        print(f"\nUnexpected error: {e}")
        
    print("\nProgram finished.")

if __name__ == "__main__":
    main()
