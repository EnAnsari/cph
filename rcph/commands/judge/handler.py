from .utils import *
from rcph.utils.get import getLastJudge, setLastJudge

def run(args):
    if args.problem:
        problem = args.problem
        if problem == 'input':
            executeInput()
            return
    else:
        problem = getLastJudge()
    
    judge(problem)
    setLastJudge(problem)