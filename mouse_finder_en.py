#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import usb.core
import usb.util

def find_usb_devices():
    """
    Lists all connected USB devices with their VID, PID and other information.
    Returns a list of found devices.
    """
    devices = []
    seen = set()

    for dev in usb.core.find(find_all=True):
        key = (dev.idVendor, dev.idProduct)
        if key in seen:
            continue
        seen.add(key)

        try:
            product = usb.util.get_string(dev, dev.iProduct) or "Unknown"
            manufacturer = usb.util.get_string(dev, dev.iManufacturer) or "Unknown"
            serial_number = usb.util.get_string(dev, dev.iSerialNumber) or "Unknown"
        except usb.core.USBError:
            product = manufacturer = serial_number = "Unavailable"

        devices.append({
            'product': product,
            'manufacturer': manufacturer, 
            'vid': dev.idVendor,
            'pid': dev.idProduct,
            'serial': serial_number,
            'vid_hex': f"0x{dev.idVendor:04X}",
            'pid_hex': f"0x{dev.idProduct:04X}"
        })
    
    return devices

def display_usb_devices(devices):
    """
    Displays information about found USB devices.
    """
    if not devices:
        print("\nNo USB devices found.")
        return
        
    print("\n" + "=" * 60)
    print("USB DEVICES FOUND")
    print("=" * 60)
    
    for i, device in enumerate(devices, 1):
        print(f"\n[{i}] {device['product']} - {device['manufacturer']}")
        print(f"    VID: {device['vid']} ({device['vid_hex']}), PID: {device['pid']} ({device['pid_hex']})")
        print(f"    Serial Number: {device['serial']}")
        print("-" * 60)

def main():
    """Main function that lists connected USB devices."""
    print("\nSearching for USB devices...")
    
    try:
        devices = find_usb_devices()
        display_usb_devices(devices)
        print(f"\nTotal devices found: {len(devices)}")
        
    except Exception as e:
        print(f"\nError while searching for USB devices: {e}")
        print("Check if you have permissions to access USB devices.")
        print("On Linux, you may need to run as root or configure udev rules.")
        
    print("\nUse this information to configure your mouse rebind.")
    print("Run the 'mouse_rebind_en.py' script to configure your mouse.")

if __name__ == "__main__":
    main()
