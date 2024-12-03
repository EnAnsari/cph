from .utils import *

def run(args):
    problem = args.problem
    if problem == '.':
        addMultiProblems()
    else:
        addProblem(problem)
