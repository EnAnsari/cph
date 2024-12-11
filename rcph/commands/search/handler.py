from .utils import readInput, connectTCBank
from rcph.utils.launcher import currentIsContest

def run(args):
    if args.connect:
        if args.connect == 'connect':
            return connectTCBank()
        else:
            raise Exception('invalid command!')

    if not currentIsContest():
        raise Exception('You are not in a contest directory!')
    
    readInput()