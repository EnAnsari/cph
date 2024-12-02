from rcph.utils.imports import print_error, inspect
from rcph.utils.launcher import isDevMode
from rcph.core.parser import create_parser

def run():
    parser = create_parser()
    args = parser.parse_args()

    if args.command:
        func = args.func
        if len(inspect.signature(func).parameters) == 0:
            func()  # Call without arguments
        else:
            func(args)  # Call with args
    else:
        parser.print_help()


def main():
    if not isDevMode():
        try:
            run()
        except Exception as e:
            print_error(str(e))
    else:
        run()


if __name__ == "__main__":
    main()
