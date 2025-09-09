# setup.py

from setuptools import setup, find_packages

setup(
    name="stegotool",
    version="1.0.0",
    author="Shantanu Verma",
    author_email="vshantanu90@gmail.com", 
    description="Educational steganography & payload demonstration tool",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/shantanu0321/Stegotool",
    packages=find_packages(),
    python_requires=">=3.8",
    install_requires=[
        "pillow",       # For image processing
        "psutil",       # For system info and processes
        "netifaces",    # For network interfaces
    ],
    entry_points={
        "console_scripts": [
            "stegotool=stegotool.cli:main",  # Run 'stegotool' in terminal
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
