# StegoTool Usage Guide 🛠️

This guide explains **step-by-step how to use StegoTool** for hiding messages, extracting them, and running payloads.

---

## Quick Command Cheat Sheet ⚡

| Action                     | Command Example |
|-----------------------------|----------------|
| Hide a message in an image  | `python -m stegotool.cli hide -i input.png -m "Secret" -o output.png` |
| Extract a message           | `python -m stegotool.cli extract -i output.png` |
| List available payloads     | `python -m stegotool.cli payload --list` |
| Run a payload               | `python -m stegotool.cli payload --type system_info` |

---

### 1. Installation

Clone the repository and install dependencies:

```
git clone https://github.com/shantanu0321/Stegotool.git
cd Stegotool
pip install -r requirements.txt
```

---

### 2. Hide Data in an Image

Hide a secret message inside an image.

Copy code
`python -m stegotool.cli hide -i <input_image> -m "<your_message>" -o <output_image>`

Example:

Copy code
`python -m stegotool.cli hide -i mypic.png -m "Hello World" -o secret.png`

`-i` → Input image file

`-m` → Message to hide

`-o` → Output image file

---

### 3. Extract Data from an Image
   
Extract a hidden message from an image.

Copy code
`python -m stegotool.cli extract -i <image_with_hidden_message>`

Example:

Copy code
`python -m stegotool.cli extract -i secret.png`

---

### 4. List Available Payloads

To see all payloads you can run:


Copy code
`python -m stegotool.cli payload --list`

 Available Payloads

| Payload Type       | Description                               | 
|-------------------|--------------------------------------------|
| System Info        | OS, IP, hostname                          |
| File Access        | Downloads folder, home directory walk     | 
| Running Processes  | Lists all running system processes        |
| USB Detection      | Lists connected USB storage               | 
| Screenshot         | Captures current screen and saves as PNG  | 
| EXIF Data          | Extracts metadata from images             | 
| Network Scan       | Scans local network for live hosts        | 
| Upload (Demo)      | Simulates sending data to your server     | 
---

### 5. Run a Payload

Run any payload by specifying its type:

Copy code
`python -m stegotool.cli payload --type <payload_type>`

Example:

copy code
`python -m stegotool.cli payload --type system_info`

Replace system_info with any payload from the list above.

---

### 6. Example Workflow

Hide a secret message:

Copy code
`python -m stegotool.cli hide -i mypic.png -m "Hello World" -o secret.png`

Extract the message:

Copy code
`python -m stegotool.cli extract -i secret.png`

Run a demo payload:

Copy code
`python -m stegotool.cli payload --type network_scan`

---

### 7. Notes
This tool is free to use.

All payloads are safe and demo-only; no real system data is sent anywhere.

Make sure Python 3.10+ is installed for proper compatibility.

---

### 8. Contributing
Fork the repo and submit a PR.

Report bugs or request features via GitHub issues.

