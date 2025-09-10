# stegotool/__init__.py

"""
StegoTool v1
Educational steganography & payload demonstration tool.

Modules:
- cli: Command-line interface
- payload: Predefined payload functions
- stego: Hide & extract data from images
"""

from .payload import PAYLOADS
from .stego import hide_message, extract_message

__version__ = "1.0"
__all__ = ["PAYLOADS", "hide_message", "extract_message"]
