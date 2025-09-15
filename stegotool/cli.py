# stegotool/cli.py

import argparse
import os
from .payload import PAYLOADS, run_payload, run_all_payloads
from .stego import hide_message, extract_message


def main():
    parser = argparse.ArgumentParser(
        description="StegoTool CLI - Educational Steganography & Payload Demonstration Tool"
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    # ---- Run a specific payload ----
    run_parser = subparsers.add_parser("run-payload", help="Run a specific payload")
    run_parser.add_argument("--type", required=True, choices=PAYLOADS.keys(), help="Payload type")
    run_parser.add_argument("--folder-path", help="For folder_listing payload")
    run_parser.add_argument("--image-path", help="For exif payload")

    # ---- Embed payload ----
    embed_parser = subparsers.add_parser("embed-payload", help="Embed payload(s) into an image")
    embed_parser.add_argument("--type", choices=PAYLOADS.keys(), help="Payload type")
    embed_parser.add_argument("--all", action="store_true", help="Embed all payloads")
    embed_parser.add_argument("--folder-path", help="For folder_listing payload")
    embed_parser.add_argument("--image-path", help="For exif payload")
    embed_parser.add_argument("-i", "--input", required=True, help="Input image path")
    embed_parser.add_argument("-o", "--output", required=True, help="Output image path")

    # ---- Extract payload ----
    extract_parser = subparsers.add_parser("extract-payload", help="Extract hidden payload from image")
    extract_parser.add_argument("-i", "--input", required=True, help="Stego image path")
    extract_parser.add_argument("-o", "--output", required=True, help="Save extracted data to file")

    args = parser.parse_args()

    # ----------------------------
    # Run single payload
    # ----------------------------
    if args.command == "run-payload":
        kwargs = {}
        if args.type == "folder_listing" and args.folder_path:
            kwargs["folder_path"] = args.folder_path
        elif args.type == "exif" and args.image_path:
            kwargs["image_path"] = args.image_path

        result = run_payload(args.type, **kwargs)
        print(f"[+] Payload result ({args.type}):\n{result}")

    # ----------------------------
    # Embed payload(s)
    # ----------------------------
    elif args.command == "embed-payload":
        kwargs = {
            "folder_path": args.folder_path,
            "image_path": args.image_path
        }

        if args.all:
            print("[*] Running all payloads...")
            results = run_all_payloads(**kwargs)
            combined = []
            for key, output in results.items():
                combined.append(f"=== {key.upper()} ===\n{output}\n")
            final_message = "\n".join(combined)
        else:
            if not args.type:
                print("[!] Error: You must specify --type or --all")
                return

            payload_kwargs = {}
            if args.type == "folder_listing" and args.folder_path:
                payload_kwargs["folder_path"] = args.folder_path
            elif args.type == "exif" and args.image_path:
                payload_kwargs["image_path"] = args.image_path

            result = run_payload(args.type, **payload_kwargs)
            final_message = f"=== {args.type.upper()} ===\n{result}"

        # Embed data into image
        try:
            hide_message(args.input, args.output, final_message)
            print(f"[+] Payload embedded into image: {args.output}")
        except Exception as e:
            print(f"[!] Failed to embed payload: {e}")

    # ----------------------------
    # Extract payload
    # ----------------------------
    elif args.command == "extract-payload":
        try:
            message = extract_message(args.input)
            with open(args.output, "w", encoding="utf-8") as f:
                f.write(message)
            print(f"[+] Extracted message saved to: {args.output}")
        except Exception as e:
            print(f"[!] Failed to extract message: {e}")


if __name__ == "__main__":
    main()
