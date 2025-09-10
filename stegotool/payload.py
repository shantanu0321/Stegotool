# stegotool/payload.py
import platform
import socket
import os
from pathlib import Path
from datetime import datetime

def system_info() -> str:
    """Return a short string with OS/hostname/IP info."""
    try:
        ip = socket.gethostbyname(socket.gethostname())
    except Exception:
        ip = "N/A"
    parts = [
        f"CollectedAt: {datetime.utcnow().isoformat()}Z",
        f"OS: {platform.system()} {platform.release()}",
        f"Platform: {platform.platform()}",
        f"Hostname: {platform.node()}",
        f"LocalIP: {ip}",
    ]
    return "\n".join(parts)

def folder_listing(folder_path: str, limit: int = 20) -> str:
    """Return newline-separated listing of up to `limit` files in the folder."""
    p = Path(folder_path).expanduser()
    if not p.exists() or not p.is_dir():
        return f"Folder not found: {folder_path}"
    items = []
    for idx, entry in enumerate(sorted(p.iterdir(), key=lambda x: x.name)):
        if idx >= limit:
            break
        items.append(entry.name)
    return f"Listing for {str(p)} (first {limit} entries):\n" + ("\n".join(items) if items else "[empty]")

# Registry (only safe payloads)
PAYLOADS = {
    "system_info": ("System Info (OS, Hostname, Local IP)", system_info),
    "folder_listing": ("Folder Listing (user-specified path)", folder_listing),
}

def list_payloads() -> str:
    lines = []
    for key, (desc, _) in PAYLOADS.items():
        lines.append(f"{key:14} - {desc}")
    return "\n".join(lines)

def run_payload(name: str, **kwargs) -> str:
    if name not in PAYLOADS:
        raise ValueError(f"Unknown payload: {name}")
    func = PAYLOADS[name][1]
    return func(**kwargs) if kwargs else func()
