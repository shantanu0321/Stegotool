import os, platform, socket, subprocess
from pathlib import Path
from PIL import ImageGrab, Image
import psutil

def system_info():
    print("\n[🧠] System Info")
    print("  OS:", platform.system(), platform.release())
    print("  Hostname:", socket.gethostname())
    try:
        ip = socket.gethostbyname(socket.gethostname())
        print("  IP Address:", ip)
    except:
        print("  IP Address: unavailable")

def file_access():
    print("\n[📂] File Access")
    home = Path.home()
    downloads = home / "Downloads"
    print("  Home Directory:", home)
    if downloads.exists():
        print("  Downloads folder contents:")
        for f in downloads.iterdir():
            print("   -", f)
    else:
        print("  No Downloads folder found.")

def list_processes():
    print("\n[📋] Running Processes")
    for proc in psutil.process_iter(['pid', 'name']):
        print(f"  PID {proc.info['pid']} - {proc.info['name']}")

def detect_usb():
    print("\n[💾] USB Devices")
    system = platform.system()
    try:
        if system == "Windows":
            output = subprocess.check_output(
                "wmic logicaldisk get name, drivetype", shell=True
            ).decode()
            for line in output.split("\n"):
                if "2" in line:
                    print(" ", line.strip())
        elif system == "Linux":
            output = subprocess.check_output(
                "lsblk -o NAME,MOUNTPOINT", shell=True
            ).decode()
            for line in output.split("\n"):
                if "/media" in line or "/mnt" in line:
                    print(" ", line.strip())
        else:
            print("  [!] USB detection not implemented for this OS.")
    except Exception as e:
        print("  [!] Error:", e)

def take_screenshot(output_file="screenshot.png"):
    print("\n[🖼] Taking Screenshot...")
    try:
        img = ImageGrab.grab()
        img.save(output_file)
        print(f"  Screenshot saved as {output_file}")
    except Exception as e:
        print("  [!] Failed:", e)

def extract_exif(image_path):
    print("\n[🧬] EXIF Metadata")
    try:
        img = Image.open(image_path)
        exif = img.getexif()
        if not exif:
            print("  No EXIF metadata found.")
            return
        for tag_id, value in exif.items():
            print(f"  {tag_id}: {value}")
    except Exception as e:
        print("  [!] Error:", e)

def network_scan(subnet="192.168.1.0/24"):
    print("\n[🌐] Network Scan")
    print(f"  Scanning {subnet} for live hosts...")
    base_ip = subnet.rsplit(".", 1)[0]
    for i in range(1, 10):
        ip = f"{base_ip}.{i}"
        result = os.system(f"ping -c 1 -w 1 {ip} > /dev/null 2>&1")
        if result == 0:
            print(f"  [+] Host UP: {ip}")

def simulate_upload():
    print("\n[🚨] Upload Simulation")
    print("  Simulating data upload to https://example.com/demo ... DONE ✅")
