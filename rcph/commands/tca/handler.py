from .utils import *
from rcph.config.constant import *

def run(args):
    problem = args.problem
    if problem == '.':
        totalAdding()
    elif problem in [COMMANDS.DELETE, COMMANDS.CLEAR]:
        clearTestCases()
    elif problem == COMMANDS.DOMJUDGE:
        domjudge()
    else:
        createTest(problem)