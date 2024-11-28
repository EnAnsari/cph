from .utils import *


def run(args):
    problem = args.problem
    if problem == '.':
        totalAdding()
    elif problem == 'domjudge':
        domjudge()
    else:
        createTest(problem)