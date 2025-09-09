from setuptools import setup, find_packages

setup(
    name="stegotool",
    version="1.0.0",
    packages=find_packages(),
    install_requires=[
        "pillow",
        "psutil"
    ],
    entry_points={
        "console_scripts": [
            "stegotool=stegotool.cli:main",
        ],
    },
    license="MIT",
    description="StegoTool - Educational Steganography and Payload Simulator",
    author="Shantanu Raj Verma",
)
