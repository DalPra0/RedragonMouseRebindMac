# Mouse Rebind

> [README em Português](README.pt-BR.md) também disponível.

A Python tool for identifying and reconfiguring USB mouse devices by sending custom commands via the HID (Human Interface Device) interface.

## 🔍 Features

- **USB Device Identification**: Locates all connected USB devices and displays detailed information (VID, PID, manufacturer, etc.)
- **Automatic Conversion**: Converts values between decimal and hexadecimal
- **Interactive Interface**: Requests all necessary information from the user, no need to edit source code
- **HID Control**: Sends custom control commands to USB devices
- **Multi-language Support**: Available in English and Portuguese

## 📋 Prerequisites

- Python 3.6 or higher
- Libraries: `pyusb` (automatically installed via pip)
- Access to USB devices (administrator permissions or udev rules on Linux)

## 🚀 Installation

### 1. Clone the repository

```bash
git clone https://github.com/yourusername/mouse-rebind.git
cd mouse-rebind
```

### 2. Install dependencies

Method 1: Using pip directly:
```bash
pip install -r requirements.txt
```

Method 2: Installing as a Python package:
```bash
pip install -e .
```

### 3. Permissions (Linux only)

On Linux, by default, regular users don't have permission to access USB devices directly. You have two options:

**Option 1:** Run scripts as root (not recommended for regular use):
```bash
sudo python3 mouse_finder.py
sudo python3 mouse_rebind.py
```

**Option 2 (Recommended):** Configure udev rules to allow access to your device:

1. Copy the rules file to the correct directory:
```bash
sudo cp 99-mouse-rebind.rules /etc/udev/rules.d/
```

2. Edit the file to add your device IDs:
```bash
sudo nano /etc/udev/rules.d/99-mouse-rebind.rules
```

3. Reload the rules:
```bash
sudo udevadm control --reload-rules
sudo udevadm trigger
```

## 📖 How to use

### Step 1: Identify your device

Run the identification script to locate your mouse:

```bash
# English version
python mouse_finder_en.py

# Portuguese version
python mouse_finder.py
```

Note down the VID (Vendor ID) and PID (Product ID) of your mouse, you'll need these values.

**Example output:**
```
=============================================================
USB DEVICES FOUND
=============================================================

[1] Gaming Mouse - GameTech
    VID: 9639 (0x25A7), PID: 64008 (0xFA08)
    Serial Number: 123456789
------------------------------------------------------------
```

### Step 2: Configure your mouse

Run the rebind script and follow the interactive instructions:

```bash
# English version
python mouse_rebind_en.py

# Portuguese version
python mouse_rebind.py
```

The script will:
1. Ask for the VID and PID of your mouse
2. Ask which commands you want to send
3. Send the commands to the device

**Example interaction:**
```
=============================================================
USB MOUSE REBIND CONFIGURATION
=============================================================

This script sends commands to configure your USB mouse.
If you don't know your mouse's VID/PID, run 'mouse_finder_en.py' first.

------------------------------------------------------------
DEVICE CONFIGURATION
------------------------------------------------------------
Enter mouse VID (decimal or hex) [9639]: 
Enter mouse PID (decimal or hex) [64008]: 

VID: 9639 (0x25A7)
PID: 64008 (0xFA08)
Enter interface number [0]: 
Enter Report Type [0x0300]: 

Enter payload as a sequence of bytes (hexadecimal or decimal values).
For example: 0x01 0x00 0x04 or 1 0 4
Payload: 0x01 0x00 0x04

------------------------------------------------------------
CONFIGURATION SUMMARY
------------------------------------------------------------
VID: 9639 (0x25A7)
PID: 64008 (0xFA08)
Interface: 0
Report Type: 768 (0x0300)
Payload: ['0x1', '0x0', '0x4']

Confirm and send command? (y/n): y

Finding device with VID=0x25A7, PID=0xFA08...
Device found!
Configuring device...
Sending command: ['0x1', '0x0', '0x4']
Command sent successfully! Bytes transferred: 3

Command processed successfully!

Program finished.
```

## 🔧 Customization

The rebind script accepts different types of commands, depending on your mouse. Here are some common examples:

- **Change DPI**: The exact format depends on your mouse manufacturer
- **Reprogram buttons**: Set new functions for mouse buttons
- **Configure lighting**: Change colors or lighting effects (on RGB mice)

## 📝 Important notes

1. **Compatibility**: Not all mice support customization via USB HID. Generally, gaming and high-performance mice are more likely to support these commands.

2. **Manufacturer protocol**: Each manufacturer has its own protocol for device control. The exact commands (payload) vary according to the mouse model and brand.

3. **Backup settings**: Always note your original settings before making changes, in case you need to revert.

4. **Windows**: On Windows systems, you may need to install WinUSB or libusb-win32 drivers for the pyusb library to work correctly.

## 🛠️ Troubleshooting

### "Device not found"
- Check if the device is connected
- Make sure VID and PID values are correct
- On Linux, check permissions (udev rules or run as root)

### "Error sending command"
- Check if the payload is correct for your mouse model
- Some mice require specific interface or report type settings

### "Permission denied" on Linux
- Configure udev rules as described in the installation section
- Alternatively, run the script as root (`sudo python mouse_rebind_en.py`)

### Windows issues
- Install libusb drivers for Windows
- Run the command prompt as administrator

### Module import errors
- Make sure the pyusb library is installed: `pip install pyusb`

## 📚 Additional resources

- [PyUSB library documentation](https://github.com/pyusb/pyusb)
- [USB HID specification](https://www.usb.org/hid)
- [HID device standards](https://www.usb.org/document-library/device-class-definition-hid-111)

## 📄 License

This project is licensed under the [MIT License](LICENSE) - see the LICENSE file for details.

## 🤝 Contributions

Contributions are welcome! Feel free to open issues and pull requests.

1. Fork the project
2. Create your Feature Branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the Branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request
