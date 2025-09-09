import argparse
import sys
from stegotool.payload import run_payload, list_payloads
from stegotool.stego import hide_message, extract_message


def main():
    parser = argparse.ArgumentParser(
        prog="stegotool",
        description="StegoTool - Hide messages in images, extract them, and run payload demos"
    )
    subparsers = parser.add_subparsers(dest="command")

    # --- Hide Command ---
    hide_parser = subparsers.add_parser("hide", help="Hide a message in an image")
    hide_parser.add_argument("-i", "--input", required=True, help="Input image")
    hide_parser.add_argument("-m", "--message", required=True, help="Message to hide")
    hide_parser.add_argument("-o", "--output", required=True, help="Output image with hidden message")

    # --- Extract Command ---
    extract_parser = subparsers.add_parser("extract", help="Extract a message from an image")
    extract_parser.add_argument("-i", "--input", required=True, help="Image containing hidden message")
    extract_parser.add_argument("-o", "--output", help="Optional file to save extracted data")

    # --- Payload Command ---
    payload_parser = subparsers.add_parser("payload", help="Run or list available payloads")
    payload_parser.add_argument("--list", action="store_true", help="List all available payloads")
    payload_parser.add_argument("--type", help="Run a specific payload (e.g., system_info)")

    # --- Embed Payload Command ---
    embed_parser = subparsers.add_parser("embed-payload", help="Run a payload and embed its output into an image")
    embed_parser.add_argument("--type", required=True, help="Payload type to run")
    embed_parser.add_argument("-i", "--input", required=True, help="Input image")
    embed_parser.add_argument("-o", "--output", required=True, help="Output image with embedded payload data")

    args = parser.parse_args()

    # --- Hide Logic ---
    if args.command == "hide":
        try:
            hide_message(args.input, args.message, args.output)
            print(f"[+] Message hidden successfully in {args.output}")
        except Exception as e:
            print(f"[!] Error: {e}")

    # --- Extract Logic ---
    elif args.command == "extract":
        try:
            message = extract_message(args.input)
            if args.output:
                with open(args.output, "w", encoding="utf-8") as f:
                    f.write(message)
                print(f"[+] Extracted message saved to {args.output}")
            else:
                print(f"[+] Extracted message:\n{message}")
        except Exception as e:
            print(f"[!] Error: {e}")

    # --- Payload Logic ---
    elif args.command == "payload":
        if args.list:
            print("\nAvailable Payloads:")
            print(list_payloads())
        elif args.type:
            try:
                output = run_payload(args.type)
                print(f"[+] Payload ({args.type}) output:\n{output}")
            except Exception as e:
                print(f"[!] Error: {e}")
        else:
            print("[!] Please specify --list or --type")

    # --- Embed Payload Logic ---
    elif args.command == "embed-payload":
        try:
            payload_output = run_payload(args.type)
            hide_message(args.input, payload_output, args.output)
            print(f"[+] Payload '{args.type}' embedded into {args.output}")
        except Exception as e:
            print(f"[!] Error: {e}")

    else:
        parser.print_help()


if __name__ == "__main__":
    sys.exit(main())
