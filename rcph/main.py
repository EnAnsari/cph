import argparse
from rcph.commands.hello import run as hello_runner

def main():
    parser = argparse.ArgumentParser(description="cph CLI Tool")

    subparsers = parser.add_subparsers(dest="command", help="Subcommands")

    hello_parser = subparsers.add_parser("hello", help="Print hello world")
    hello_parser.set_defaults(func=hello_runner)

    args = parser.parse_args()

    if args.command:
        # Execute the function associated with the command
        args.func()
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
    