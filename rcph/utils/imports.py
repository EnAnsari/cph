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
import prompt_toolkit
import tqdm
import re
import selenium
import bs4
# import urllib
# import importlib.resources as pkg_resources

from prompt_toolkit import prompt
from prompt_toolkit.styles import Style
from prompt_toolkit.history import InMemoryHistory
from prompt_toolkit.completion import Completer, Completion

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup

from pathlib import Path

__all__ = ['prompt_toolkit', 'prompt', 'Style', 'InMemoryHistory', 'Completer', 'Completion',
    'bs4', 'selenium', 'webdriver', 'Service', 'By', 'Options', 'BeautifulSoup',
    'pathlib', 'Path',
    're', 'argparse', 'sys', 'os', 'json', 'shutil', 'random', 'datetime', 'zipfile', 'inspect', 'subprocess', 'tqdm', 'print_error']

from .tools.color import colored_text
def print_error(message):
    """Print an error message and exit."""
    print(f"Error: {colored_text(message, 'red')}")
    sys.exit(1)
