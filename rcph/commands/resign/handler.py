from .utils import *
from rcph.utils.launcher import checkExistenceProblem, currentIsContest

def run(args):
    if not currentIsContest():
        raise Exception('You are not in a contest directory!')
    
    if args.problem == '.':
        multiResign()
    else:
        if not checkExistenceProblem(args.problem):
            raise Exception(f'problem {args.problem} doesn\'t exist!')
        resignProblem(args.problem)