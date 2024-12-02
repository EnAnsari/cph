from rcph.utils.tools.color import colored_text
from .utils import *
from rcph.config.constant import *
from rcph.utils.launcher import isDevMode

def createContestInFolder(folder_path, parent, test):
    contest_info = getContestInfo()
    makeRcphFolder(folder_path, contest_info, parent)
    makeProblemCodes(folder_path, contest_info)
    if not isDevMode and not test:
        updateDBcontest(folder_path)
    print(f'\nyour contest created {colored_text("successfully", "green", "bold")} by {len(contest_info["problems"])} problem!')


def createContestByFolder(folder_name, parent, test):
    folder_path = os.path.join(os.getcwd(), folder_name)
    makeFolder(folder_name)
    createContestInFolder(folder_path, parent, test)
    makeTemplateCode(folder_path)
    print(f'please run this command to enter your contest directory:')
    print(colored_text(f'cd ./{folder_name}', 'yellow', 'bold'))


def run(args):
    folder_name = args.folder_name
    test_mode = True if args.test and args.test == 'test' else False
    if args.parent:
        parent = os.path.join(os.getcwd(), args.parent, RCPH_FOLDER, PARENT_PORTAL)
        if os.path.exists(parent):
            with open(parent, 'r') as parent_file:
                parent = parent_file.read()
        else:
            raise FileExistsError('parent portal does not exist!')
    else:
        parent = ''

    if(folder_name == '.'):
        createContestInFolder(os.getcwd(), parent, test_mode)
    else:
        createContestByFolder(folder_name, parent, test_mode)
