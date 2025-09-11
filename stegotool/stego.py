# stegotool/stego.py

from PIL import Image

# -----------------------------
# Binary Encoding/Decoding Helpers
# -----------------------------

def str_to_bin(message: str) -> str:
    """Convert a string to a binary string."""
    return ''.join(format(ord(char), '08b') for char in message)

def bin_to_str(binary: str) -> str:
    """Convert a binary string to a regular string."""
    chars = [binary[i:i+8] for i in range(0, len(binary), 8)]
    return ''.join(chr(int(char, 2)) for char in chars if len(char) == 8)

# -----------------------------
# Core Stego Functions
# -----------------------------

def hide_message(input_image_path: str, output_image_path: str, message: str):
    """Embed the binary message into the least significant bits of an image."""
    img = Image.open(input_image_path)
    if img.mode != 'RGB':
        img = img.convert('RGB')
    pixels = list(img.getdata())

    # Convert message to binary and add delimiter
    binary_message = str_to_bin(message) + '1111111111111110'  # End marker

    binary_index = 0
    new_pixels = []

    for pixel in pixels:
        if binary_index >= len(binary_message):
            new_pixels.append(pixel)
            continue

        r, g, b = pixel
        r_bin = format(r, '08b')
        g_bin = format(g, '08b')
        b_bin = format(b, '08b')

        # Modify LSBs with message bits
        if binary_index < len(binary_message):
            r_bin = r_bin[:-1] + binary_message[binary_index]
            binary_index += 1
        if binary_index < len(binary_message):
            g_bin = g_bin[:-1] + binary_message[binary_index]
            binary_index += 1
        if binary_index < len(binary_message):
            b_bin = b_bin[:-1] + binary_message[binary_index]
            binary_index += 1

        new_pixel = (int(r_bin, 2), int(g_bin, 2), int(b_bin, 2))
        new_pixels.append(new_pixel)

    # Create and save new image
    img.putdata(new_pixels)
    img.save(output_image_path)
    print(f"[+] Message successfully embedded into {output_image_path}")

def extract_message(stego_image_path: str) -> str:
    """Extract hidden binary message from image's pixel data."""
    img = Image.open(stego_image_path)
    pixels = list(img.getdata())

    binary_data = ""
    for pixel in pixels:
        for value in pixel[:3]:  # Only R, G, B (ignore alpha if present)
            binary_data += format(value, '08b')[-1]

    # Find the end delimiter
    delimiter = '1111111111111110'
    end_index = binary_data.find(delimiter)
    if end_index == -1:
        return "[!] No hidden message found."

    binary_message = binary_data[:end_index]
    return bin_to_str(binary_message)
