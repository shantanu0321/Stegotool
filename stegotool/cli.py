# stegotool/cli.py
import argparse
import sys
import textwrap
from stegotool import stego, payload
from pathlib import Path
from datetime import datetime

CONSENT_LOG = Path("consent.log")

def log_consent(action: str, details: str) -> None:
    with open(CONSENT_LOG, "a", encoding="utf-8") as f:
        f.write(f"{datetime.utcnow().isoformat()}Z | {action} | {details}\n")

def ask_consent(message: str) -> bool:
    print("\n*** CONSENT REQUIRED ***")
    print(message)
    resp = input("Do you consent? (y/N): ").strip().lower()
    return resp == 'y'

def cmd_list():
    print("Available payloads:\n")
    print(payload.list_payloads())

def cmd_extract(args):
    out = stego.extract_message(args.input)
    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(out)
        print(f"[+] Extracted payload saved to {args.output}")
    else:
        print("\n--- Extracted payload start ---")
        print(out)
        print("--- Extracted payload end ---\n")

def cmd_embed_payload(args):
    # require explicit consent
    consent_text = textwrap.dedent(f"""
    You are about to run payload '{args.type}' and embed its output into an image.
    Collected data will be:
      - {payload.PAYLOADS.get(args.type, ('Unknown',))[0]}
    The data will be stored only inside the output image file you specify.
    """)
    if not ask_consent(consent_text):
        print("Consent denied. Aborting.")
        return

    # gather payload
    if args.type == "folder_listing":
        if not args.folder:
            print("[!] folder_listing requires --folder <path>")
            return
        payload_text = payload.run_payload(args.type, folder_path=args.folder, limit=args.limit)
        details = f"type={args.type}, folder={args.folder}, limit={args.limit}"
    else:
        payload_text = payload.run_payload(args.type)
        details = f"type={args.type}"

    # embed
    try:
        stego.hide_message(args.input, payload_text, args.output)
        print(f"[+] Embedded payload into {args.output}")
        log_consent("embed-payload", details)
    except Exception as e:
        print(f"[!] Error embedding payload: {e}")

def cmd_hide(args):
    # simple consent for arbitrary message
    consent_text = "You are about to hide arbitrary text data into an image. This tool does NOT send data anywhere."
    if not ask_consent(consent_text):
        print("Consent denied. Aborting.")
        return
    try:
        stego.hide_message(args.input, args.message, args.output)
        print(f"[+] Message hidden into {args.output}")
        log_consent("hide-message", f"len={len(args.message)}")
    except Exception as e:
        print(f"[!] Error hiding message: {e}")

def main():
    parser = argparse.ArgumentParser(prog="stegotool", description="StegoTool demonstrator (safe, consented)")
    sub = parser.add_subparsers(dest="cmd")

    sub.add_parser("list-payloads", help="List available safe payloads")

    embed_p = sub.add_parser("embed-payload", help="Run a payload and embed its output into an image")
    embed_p.add_argument("--type", required=True, choices=list(payload.PAYLOADS.keys()), help="Payload key")
    embed_p.add_argument("-i", "--input", required=True, help="Cover image path (PNG preferred)")
    embed_p.add_argument("-o", "--output", required=True, help="Output image path")
    embed_p.add_argument("--folder", help="Folder path (for folder_listing payload)")
    embed_p.add_argument("--limit", type=int, default=20, help="Limit files listed for folder_listing")

    hide_p = sub.add_parser("hide", help="Hide an arbitrary message into an image (consent required)")
    hide_p.add_argument("-i", "--input", required=True, help="Cover image path")
    hide_p.add_argument("-m", "--message", required=True, help="Message to hide")
    hide_p.add_argument("-o", "--output", required=True, help="Output image path")

    extract_p = sub.add_parser("extract", help="Extract hidden payload from an image")
    extract_p.add_argument("-i", "--input", required=True, help="Image with hidden payload")
    extract_p.add_argument("-o", "--output", help="Save extracted payload to file")

    args = parser.parse_args()
    if args.cmd == "list-payloads":
        cmd_list()
    elif args.cmd == "embed-payload":
        cmd_embed_payload(args)
    elif args.cmd == "hide":
        cmd_hide(args)
    elif args.cmd == "extract":
        cmd_extract(args)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
