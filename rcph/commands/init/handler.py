from rcph.utils.color import colored_text
from rcph.commands.init.utils import *

def run(args):
    folder_name = args.folder_name
    folder_path = os.path.join(os.getcwd(), folder_name)
    makeFolder(folder_name)
    contest_info = getContestInfo()
    makeRcphFolder(folder_path, contest_info)
    makeTemplateCode(folder_path)
    makeProblemCodes(folder_path, contest_info)
    addToDB(folder_path)

    print(f'\nyour contest created {colored_text("successfully", "green", "bold")} by {len(contest_info["problems"])} problem!')
    print(f'please run this command to enter your contest directory:')
    print(colored_text(f'cd ./{folder_name}', 'yellow', 'bold'))