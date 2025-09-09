# StegoTool v2

A command-line steganography tool for hiding files in images **and simulating payload attacks** .

## Features
- Hide any file inside PNG/JPG images
- Extract hidden files
- Simulate payload actions:
    - 🧠 System Info
    - 📂 File Access
    - 📋 Running Processes
    - 💾 USB Detection
    - 🖼 Screenshot
    - 🧬 EXIF Metadata Extraction
    - 🌐 Network Scan
    - 🚨 Upload Simulation

## Install
```bash
git clone https://github.com/shantanu0321/stegotool.git
cd stegotool
pip install .
```

## Usage
```bash
stegotool run-payload --system
stegotool run-payload --files
stegotool run-payload --processes
stegotool run-payload --usb
stegotool run-payload --screenshot
stegotool run-payload --exif example.jpg
stegotool run-payload --scan
stegotool run-payload --upload
```

⚠️ Disclaimer: 

This tool is developed strictly for educational and research purposes only. The author(s) of this tool shall not be held responsible or liable for any misuse, illegal activities, or damages caused by the use of this tool.

By using this tool, you agree that:

You are solely responsible for your actions.

This tool must only be used for ethical hacking, penetration testing (with proper authorization), research, or learning purposes.

Any malicious or unauthorized usage is strictly prohibited and is the sole responsibility of the user.

By downloading, installing, or using this tool, you acknowledge that you have read and understood this license and disclaimer.
