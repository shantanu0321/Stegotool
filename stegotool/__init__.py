"""
StegoTool v1
Educational steganography & payload demonstration tool.

Modules:
- cli: Command-line interface
- payload: Predefined payload functions
- stego: Hide & extract data from images
"""

from .payload import PAYLOADS, run_all_payloads
from .stego import hide_message, extract_message

__version__ = "1.0"
__all__ = ["PAYLOADS", "run_all_payloads", "hide_message", "extract_message"]
