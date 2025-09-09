import argparse
import json
from stegotool import payload

def main():
    parser = argparse.ArgumentParser(
        description="StegoTool v2 - Educational Payload Demonstration"
    )

    parser.add_argument(
        "run_payload",
        help="Specify the payload type to run",
        choices=[
            "system",
            "files",
            "processes",
            "usb",
            "screenshot",
            "exif",
            "scan",
            "upload",
        ],
    )

    parser.add_argument(
        "--image",
        help="Image path for EXIF data extraction (required for 'exif' payload)"
    )

    parser.add_argument(
        "--data",
        help="JSON string for upload simulation (required for 'upload' payload)"
    )

    args = parser.parse_args()

    # Run selected payload
    if args.run_payload == "exif":
        if not args.image:
            print("❌ Please provide --image for EXIF payload")
            return
        result = payload.exif_data(args.image)

    elif args.run_payload == "upload":
        if not args.data:
            print("❌ Please provide --data for upload simulation")
            return
        try:
            data = json.loads(args.data)
        except json.JSONDecodeError:
            print("❌ Invalid JSON format in --data")
            return
        result = payload.upload_simulation(data)

    else:
        func = payload.PAYLOADS[args.run_payload]
        result = func()

    print(json.dumps(result, indent=4))


if __name__ == "__main__":
    main()
