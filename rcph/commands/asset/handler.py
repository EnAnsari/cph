from .launch import makeConnection, getAssetFile
from .save import checkExistence, explore, fileSaving
def run(args):
    if args.subcommand == 'connect':
        makeConnection()
    elif args.subcommand in ['save', '+']:
        if not args.file:
            raise Exception('file switch is required for save operation!')
        file_path = checkExistence(args.file)
        des_path = explore()
        fileSaving(file_path, des_path)
    else:
        getAssetFile()
