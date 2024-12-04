from .utils import *

def run(args):
    connect = True if args.connect and args.connect == 'connect' else False

    if connect:
        makeConnection()
    else:
        getAssetFile()
