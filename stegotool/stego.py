# stegotool/stego.py
from PIL import Image
import math

def _text_to_bits(text: str) -> str:
    return ''.join(format(ord(c), '08b') for c in text)

def _bits_to_text(bits: str) -> str:
    chars = [bits[i:i+8] for i in range(0, len(bits), 8)]
    text = ''
    for b in chars:
        if len(b) < 8:
            break
        ch = chr(int(b, 2))
        if ch == '\0':  # terminator
            break
        text += ch
    return text

def hide_message(input_path: str, message: str, output_path: str) -> None:
    """
    Hide `message` string into the image at `input_path` and save to `output_path`.
    Adds a null terminator '\0' to mark the end of the message.
    """
    img = Image.open(input_path)
    if img.mode not in ('RGB', 'RGBA'):
        img = img.convert('RGB')

    width, height = img.size
    max_bytes = width * height * 3 // 8  # approx
    message_with_term = message + '\0'
    if len(message_with_term) > max_bytes:
        raise ValueError(f"Message too large to hide in this image (max {max_bytes} chars).")

    bitstream = _text_to_bits(message_with_term)
    pixels = list(img.getdata())
    new_pixels = []
    bit_index = 0
    total_bits = len(bitstream)

    for pix in pixels:
        r, g, b = pix[:3]
        r = (r & ~1) | (int(bitstream[bit_index]) if bit_index < total_bits else r & 1)
        bit_index += 1 if bit_index < total_bits else 0

        g = (g & ~1) | (int(bitstream[bit_index]) if bit_index < total_bits else g & 1)
        bit_index += 1 if bit_index < total_bits else 0

        b = (b & ~1) | (int(bitstream[bit_index]) if bit_index < total_bits else b & 1)
        bit_index += 1 if bit_index < total_bits else 0

        if len(pix) == 4:
            new_pixels.append((r, g, b, pix[3]))
        else:
            new_pixels.append((r, g, b))

    encoded = Image.new(img.mode, img.size)
    encoded.putdata(new_pixels)
    encoded.save(output_path)

def extract_message(input_path: str) -> str:
    """
    Extract hidden text from `input_path`. Stops at null terminator.
    """
    img = Image.open(input_path)
    if img.mode not in ('RGB', 'RGBA'):
        img = img.convert('RGB')

    pixels = list(img.getdata())
    bits = ''
    for pix in pixels:
        r, g, b = pix[:3]
        bits += str(r & 1)
        bits += str(g & 1)
        bits += str(b & 1)

    text = _bits_to_text(bits)
    return text
