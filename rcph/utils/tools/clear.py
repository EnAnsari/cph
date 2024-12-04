from ..imports import os

def clear_terminal():
    # Check the operating system and run the appropriate command
    if os.name == 'posix':
        os.system('clear')  # For Linux, macOS, and other POSIX systems
    elif os.name == 'nt':
        os.system('cls')    # For Windows systems