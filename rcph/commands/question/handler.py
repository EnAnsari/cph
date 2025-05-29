from .utils import addProblem, addMultiProblems, delProblem, delMultiProblems, queraAddProblem
from rcph.utils.launcher import currentIsContest, checkExistenceProblem
from rcph.config.constant import *

def run(args):
    if not currentIsContest():
        raise Exception('You are not in a contest directory!')

    if args.operation in COMMANDS.ADD:
        if args.problem == '.':
            addMultiProblems()
        elif checkExistenceProblem(args.problem):
            raise Exception(f'problem {args.problem} exist before!')
        else:
            if args.quera:
                queraAddProblem(args.problem)
            else:
                addProblem(args.problem)
    elif args.operation in COMMANDS.DELETE:
        if args.problem == '.':
            delMultiProblems()
        elif not checkExistenceProblem(args.problem):
            raise Exception(f'problem {args.problem} does not exist!')
        else:
            delProblem(args.problem)
    else:
        raise Exception('invalid command for operation (add or rm)')
