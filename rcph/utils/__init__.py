import argparse
import sys
import os
import json
import shutil
import random
import datetime

__all__ = ['argparse', 'sys', 'os', 'json', 'shutil', 'random', 'datetime', 'print_error']

from rcph.utils.color import colored_text
def print_error(message):
    """Print an error message and exit."""
    print(f"Error: {colored_text(message, 'red')}")
    sys.exit(1)
