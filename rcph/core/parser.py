from rcph.utils import argparse
from rcph.utils.hello import run as hello_runner
from rcph.commands.init.handler import run as init_runner

def create_parser():
    parser = argparse.ArgumentParser(
        description="Welcome to rcph! A CLI tool for competitive programming.",
        epilog="for more information visit: https://github.com/EnAnsari/cph",
    )
    subparsers = parser.add_subparsers(dest="command", help="Available subcommands")

    # Add the 'hello' subcommand
    hello_parser = subparsers.add_parser("hello", help="rcph hello to you!")
    hello_parser.set_defaults(func=hello_runner)

    # Add the 'init' subcommand
    init_parser = subparsers.add_parser("init", help="Initialize configuration")
    init_parser.add_argument('folder_name', help='Name of the folder to initialize.')
    init_parser.set_defaults(func=init_runner)

    return parser
