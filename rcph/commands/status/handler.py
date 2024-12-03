from .utils import *

def run(args):
    problem = args.problem

    if problem == '.':
        setMultiStatus()
    else:
        checkExistenceProblem(problem)
        setStatus(problem)