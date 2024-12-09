from .utils import *
from rcph.utils.launcher import currentIsContest

def run():
    if not currentIsContest():
        raise Exception('You are not in a contest directory!')

    print('codeforces parser is not developed yet!')