from .utils import readInput
from rcph.utils.launcher import currentIsContest

def run():
    if not currentIsContest():
        raise Exception('You are not in a contest directory!')
    
    readInput()