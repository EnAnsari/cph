from .utils import *
from rcph.config.constant import *
from rcph.utils.launcher import getParents, getGlobaltConfig

def run(args):
    folder_name = args.folder_name
    parent = args.parent if args.parent else getGlobaltConfig()[DICT.DEFAULT_PARENT]
    test_mode = True if args.test == COMMANDS.TEST else False

    if not parent in getParents():
        raise Exception(f'{parent} not exist in parents list!')

    if(folder_name == '.'):
        createContestInFolder(os.getcwd(), parent, test_mode)
    else:
        createContestByFolder(folder_name, parent, test_mode)
