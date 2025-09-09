import argparse
from stegotool.payload import (
    system_info, file_access, list_processes,
    detect_usb, take_screenshot, extract_exif,
    network_scan, simulate_upload
)

def main():
    parser = argparse.ArgumentParser(description="StegoTool - Demo Payload CLI")
    subparsers = parser.add_subparsers(dest="command")

    payload_parser = subparsers.add_parser("run-payload", help="Run demo payloads")
    payload_parser.add_argument("--system", action="store_true", help="System info")
    payload_parser.add_argument("--files", action="store_true", help="File access")
    payload_parser.add_argument("--processes", action="store_true", help="Running processes")
    payload_parser.add_argument("--usb", action="store_true", help="Detect USB devices")
    payload_parser.add_argument("--screenshot", action="store_true", help="Take screenshot")
    payload_parser.add_argument("--exif", type=str, help="Extract EXIF from image")
    payload_parser.add_argument("--scan", action="store_true", help="Network scan")
    payload_parser.add_argument("--upload", action="store_true", help="Simulate upload")

    args = parser.parse_args()

    if args.command == "run-payload":
        if args.system:
            system_info()
        if args.files:
            file_access()
        if args.processes:
            list_processes()
        if args.usb:
            detect_usb()
        if args.screenshot:
            take_screenshot()
        if args.exif:
            extract_exif(args.exif)
        if args.scan:
            network_scan()
        if args.upload:
            simulate_upload()
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
