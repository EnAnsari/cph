from .utils import *
from rcph.utils.launcher import getLastJudge, setLastJudge
from rcph.config.constant import *

def run(args):
    if args.problem:
        problem = args.problem
        if problem == DICT.PROBLEMS:
            executeInput()
            return
    else:
        problem = getLastJudge()
    
    judge(problem)
    setLastJudge(problem)