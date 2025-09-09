import argparse
from stegotool import hide, extract, payload

def main():
    parser = argparse.ArgumentParser(prog="stegotool", description="StegoTool CLI")
    subparsers = parser.add_subparsers(dest="command", required=True)

    # Hide command
    hide_parser = subparsers.add_parser("hide", help="Hide a message or file in an image")
    hide_parser.add_argument("-i", "--input", required=True, help="Input image path")
    hide_parser.add_argument("-m", "--message", help="Message to hide")
    hide_parser.add_argument("-f", "--file", help="File to hide")
    hide_parser.add_argument("-o", "--output", required=True, help="Output image path")

    # Extract command
    extract_parser = subparsers.add_parser("extract", help="Extract hidden data from an image")
    extract_parser.add_argument("-i", "--input", required=True, help="Input image path")
    extract_parser.add_argument("-o", "--output", help="Output file (optional)")

    # Payload command
    payload_parser = subparsers.add_parser("payload", help="Run or list payloads")
    payload_parser.add_argument("--list", action="store_true", help="List available payloads")
    payload_parser.add_argument("--type", help="Run a specific payload")

    # NEW: Embed payload directly into image
    embed_parser = subparsers.add_parser("embed-payload", help="Run a payload and embed its output into an image")
    embed_parser.add_argument("--type", required=True, help="Payload type to run")
    embed_parser.add_argument("-i", "--input", required=True, help="Input image path")
    embed_parser.add_argument("-o", "--output", required=True, help="Output image path")

    args = parser.parse_args()

    if args.command == "hide":
        hide.hide_data(args.input, args.output, message=args.message, file_path=args.file)

    elif args.command == "extract":
        extract.extract_data(args.input, args.output)

    elif args.command == "payload":
        if args.list:
            payload.list_payloads()
        elif args.type:
            payload.run_payload(args.type)

    elif args.command == "embed-payload":
        data = payload.run_payload(args.type, return_output=True)
        hide.hide_data(args.input, args.output, message=data)
