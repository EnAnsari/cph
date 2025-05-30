from .utils import *
from rcph.utils.launcher import currentIsContest

def run(args):
    if not currentIsContest():
        raise Exception('You are not in a contest directory!')

    checkExistenceDir(args.address)
    readme_content = createReadme(args.address)
    fileWriter(args.address, readme_content)