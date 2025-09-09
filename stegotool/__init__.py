# stegotool/__init__.py

"""
StegoTool v2
Educational steganography & payload demonstration tool.

Modules:
- cli: Command-line interface
- payload: Predefined payload functions
- hide: Hide data in images
- extract: Extract data from images
"""

from .payload import PAYLOADS
from .hide import hide_data
from .extract import extract_data

__version__ = "2.0"
__all__ = ["PAYLOADS", "hide_data", "extract_data"]
