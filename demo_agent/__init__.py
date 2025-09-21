"""
Demo Agent - A Python CLI tool for code analysis and language/framework identification.
"""

__version__ = "0.1.0"
__author__ = "Raunak Singwi"

# Import main components for easy access
from .enums import Language, Framework
from .tools import *  # Import all tools if you want them available at package level

__all__ = ["Language", "Framework"]
