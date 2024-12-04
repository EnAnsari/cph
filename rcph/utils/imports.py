import argparse
import sys
import os
import json
import shutil
import random
import datetime
import zipfile
import subprocess
import inspect
import pathlib
# import importlib.resources as pkg_resources

__all__ = ['pathlib', 'argparse', 'sys', 'os', 'json', 'shutil', 'random', 'datetime', 'zipfile', 'inspect', 'subprocess', 'print_error']

from .tools.color import colored_text
def print_error(message):
    """Print an error message and exit."""
    print(f"Error: {colored_text(message, 'red')}")
    sys.exit(1)
