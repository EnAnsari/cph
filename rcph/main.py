from rcph.utils import print_error
from rcph.core.parser import create_parser

def main():
    # try:
        parser = create_parser()
        args = parser.parse_args()

        if args.command:
            args.func(args)
        else:
            parser.print_help()
    # except Exception as e:
    #     print_error(str(e))

if __name__ == "__main__":
    main()
