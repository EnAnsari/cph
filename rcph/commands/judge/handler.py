from .utils import *
from rcph.utils.launcher import getLastJudge, setLastJudge, currentIsContest, checkExistenceProblem
from rcph.config.constant import *

def run(args):
    if not currentIsContest():
        raise Exception('You are not in a contest directory!')

    problem = args.problem
    if problem:
        if problem == COMMANDS.INPUT:
            executeInput()
            return
    else:
        problem = getLastJudge()
    
    if not checkExistenceProblem(problem):
        raise Exception(f'problem {problem} doesn\'t exist!')
    
    judge(problem)
    setLastJudge(problem)