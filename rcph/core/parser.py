from rcph.utils import argparse
from rcph.utils.hello import run as hello_runner
from rcph.commands.init.handler import run as init_runner
from rcph.commands.tca.handler import run as tca_runner
from rcph.commands.judge.handler import run as judge_runner

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
    init_parser = subparsers.add_parser("init", aliases=["i"], help="Initialize configuration")
    init_parser.add_argument('folder_name', help='Name of the folder to initialize.')
    init_parser.add_argument('parent', nargs='?', help='parent portal address')
    init_parser.set_defaults(func=init_runner)

    # Add the 'tca' subcommand (test case adder)
    tca_parser = subparsers.add_parser("tca", aliases=["t"], help="test case adder")
    tca_parser.add_argument('problem', help='problem name')
    tca_parser.set_defaults(func=tca_runner)

    # Add the 'judge' subcommand
    judge_parser = subparsers.add_parser("judge", aliases=["j"], help="test case judger")
    judge_parser.add_argument('problem', nargs='?', help='problem name')
    judge_parser.set_defaults(func=judge_runner)

    return parser
