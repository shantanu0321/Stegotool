# stegotool/stego.py

from PIL import Image


def _text_to_binary(text):
    return ''.join(format(ord(c), '08b') for c in text)


def _binary_to_text(binary):
    chars = [binary[i:i+8] for i in range(0, len(binary), 8)]
    return ''.join(chr(int(b, 2)) for b in chars)


def hide_message(input_path, output_path, message):
    img = Image.open(input_path)
    encoded = img.copy()

    binary_message = _text_to_binary(message)
    binary_message += '1111111111111110'  # EOF marker

    if img.mode != 'RGB':
        raise ValueError("Image must be in RGB mode")

    data = list(encoded.getdata())
    data_len = len(data)
    pixel_index = 0
    bit_index = 0

    for pixel in data:
        if bit_index >= len(binary_message):
            break

        r, g, b = pixel
        new_rgb = []

        for color in (r, g, b):
            if bit_index < len(binary_message):
                lsb = int(binary_message[bit_index])
                new_color = (color & ~1) | lsb
                new_rgb.append(new_color)
                bit_index += 1
            else:
                new_rgb.append(color)

        data[pixel_index] = tuple(new_rgb)
        pixel_index += 1

    if bit_index < len(binary_message):
        raise ValueError("Message too long to hide in image.")

    encoded.putdata(data)
    encoded.save(output_path)


def extract_message(image_path):
    img = Image.open(image_path)
    binary_data = ""
    for pixel in img.getdata():
        for color in pixel[:3]:  # Only use RGB
            binary_data += str(color & 1)

    eof_marker = '1111111111111110'
    eof_index = binary_data.find(eof_marker)

    if eof_index == -1:
        raise ValueError("No hidden message found.")

    binary_message = binary_data[:eof_index]
    return _binary_to_text(binary_message)
