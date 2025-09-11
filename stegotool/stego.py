from PIL import Image

# End marker to signal end of hidden message in binary
END_MARKER = '1111111111111110'  # 16 bits

def hide_message(input_path, output_path, message):
    """
    Hide a text message inside an image's red channel LSB.

    Parameters:
    - input_path: str, path to input image (PNG or JPG)
    - output_path: str, path to save the output image with hidden message
    - message: str, the message to hide
    """
    try:
        img = Image.open(input_path)

        # Convert image to RGB if not already (handles PNG with alpha, grayscale, etc.)
        if img.mode != 'RGB':
            img = img.convert('RGB')

        encoded = img.copy()
        width, height = img.size
        index = 0

        # Convert message to binary string, append end marker
        binary_message = ''.join(format(ord(char), '08b') for char in message) + END_MARKER

        for y in range(height):
            for x in range(width):
                if index < len(binary_message):
                    r, g, b = img.getpixel((x, y))
                    # Set the LSB of red channel to the current bit of the message
                    r = (r & ~1) | int(binary_message[index])
                    encoded.putpixel((x, y), (r, g, b))
                    index += 1
                else:
                    # Finished embedding message
                    encoded.save(output_path)
                    return
        # In case message is longer than capacity, save what we have
        encoded.save(output_path)

    except Exception as e:
        raise RuntimeError(f"Failed to embed message: {e}")

def extract_message(image_path):
    """
    Extract a hidden message from an image's red channel LSB.

    Parameters:
    - image_path: str, path to the image containing the hidden message

    Returns:
    - Extracted message string, or error message string on failure
    """
    try:
        img = Image.open(image_path)

        # Convert to RGB if needed
        if img.mode != 'RGB':
            img = img.convert('RGB')

        binary_data = ""
        width, height = img.size

        # Extract LSB of red channel pixels into binary string
        for y in range(height):
            for x in range(width):
                r, g, b = img.getpixel((x, y))
                binary_data += str(r & 1)

        # Split binary string into bytes
        all_bytes = [binary_data[i:i+8] for i in range(0, len(binary_data), 8)]

        message = ""
        for byte in all_bytes:
            if byte == '11111110':  # Partial end marker (8 bits) indicates end
                break
            message += chr(int(byte, 2))

        return message

    except Exception as e:
        return f"Failed to extract message: {e}"
