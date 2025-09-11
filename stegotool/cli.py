# stegotool/cli.py

import argparse
import os
from .payload import PAYLOADS, run_payload, list_payloads, run_all_payloads
from .stego import hide_message, extract_message


def main():
    parser = argparse.ArgumentParser(
        description="StegoTool CLI - Educational Steganography & Payload Demonstration Tool"
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    # ---- Run single payload ----
    run_parser = subparsers.add_parser("run-payload", help="Run a specific payload")
    run_parser.add_argument("--type", required=True, choices=PAYLOADS.keys(), help="Payload type")
    run_parser.add_argument("--folder-path", help="Path for folder_listing payload")
    run_parser.add_argument("--image-path", help="Image path for exif payload")

    # ---- Embed payload ----
    embed_parser = subparsers.add_parser("embed-payload", help="Embed payload(s) into an image")
    embed_parser.add_argument("--type", choices=PAYLOADS.keys(), help="Payload type")
    embed_parser.add_argument("--all", action="store_true", help="Run all payloads")
    embed_parser.add_argument("--folder-path", help="Path for folder_listing payload")
    embed_parser.add_argument("--image-path", help="Image path for exif payload")
    embed_parser.add_argument("-i", "--input", required=True, help="Input image path")
    embed_parser.add_argument("-o", "--output", required=True, help="Output image path")

    # ---- Extract payload ----
    extract_parser = subparsers.add_parser("extract-payload", help="Extract hidden payload from an image")
    extract_parser.add_argument("-i", "--input", required=True, help="Stego image path")

    args = parser.parse_args()

    # ----------------------------
    # Run a single payload
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
    # Embed one or all payloads into image
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

            # Save to file
            txt_file = os.path.splitext(args.output)[0] + "_payloads_output.txt"
            with open(txt_file, "w", encoding="utf-8") as f:
                f.write(final_message)
            print(f"[+] All payload results saved to {txt_file}")

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

        # Embed into image
        try:
            hide_message(args.input, args.output, final_message)
            print(f"[+] Payload embedded into {args.output}")
        except Exception as e:
            print(f"[!] Failed to embed payload: {e}")

    # ----------------------------
    # Extract from image
    # ----------------------------
    elif args.command == "extract-payload":
        try:
            message = extract_message(args.input)
            print(f"[+] Extracted message:\n{message}")
        except Exception as e:
            print(f"[!] Failed to extract message: {e}")


if __name__ == "__main__":
    main()
