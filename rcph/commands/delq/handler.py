from .utils import *

def run(args):
    problem = args.problem
    if problem == '.':
        delMultiProblems()
    else:
        delProblem(problem)
