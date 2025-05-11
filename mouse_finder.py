#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import usb.core
import usb.util

def find_usb_devices():
    """
    Lista todos os dispositivos USB conectados com seus VID, PID e outras informações.
    Retorna uma lista de dispositivos encontrados.
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
    Exibe informações dos dispositivos USB encontrados.
    """
    if not devices:
        print("\nNenhum dispositivo USB encontrado.")
        return
        
    print("\n" + "=" * 60)
    print("DISPOSITIVOS USB ENCONTRADOS")
    print("=" * 60)
    
    for i, device in enumerate(devices, 1):
        print(f"\n[{i}] {device['product']} - {device['manufacturer']}")
        print(f"    VID: {device['vid']} ({device['vid_hex']}), PID: {device['pid']} ({device['pid_hex']})")
        print(f"    Número de Série: {device['serial']}")
        print("-" * 60)

def main():
    """Função principal que lista os dispositivos USB conectados."""
    print("\nBuscando dispositivos USB...")
    
    try:
        devices = find_usb_devices()
        display_usb_devices(devices)
        print(f"\nTotal de dispositivos encontrados: {len(devices)}")
        
    except Exception as e:
        print(f"\nErro ao buscar dispositivos USB: {e}")
        print("Verifique se você tem permissões para acessar dispositivos USB.")
        print("No Linux, pode ser necessário executar como root ou configurar regras udev.")
        
    print("\nUse estas informações para configurar o rebind do seu mouse.")
    print("Execute o script 'mouse_rebind.py' para configurar seu mouse.")

if __name__ == "__main__":
    main()
