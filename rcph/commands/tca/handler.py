from .utils import totalAdding, clearTestCases, domjudge, createTest
from rcph.config.constant import *
from rcph.utils.launcher import currentIsContest, checkExistenceProblem

def run(args):
    if not currentIsContest():
        raise Exception('You are not in a contest directory!')

    problem = args.problem
    if problem == '.':
        totalAdding()
    elif problem in COMMANDS.CLEAR:
        clearTestCases()
    elif problem == COMMANDS.DOMJUDGE:
        domjudge()
    elif not checkExistenceProblem(problem):
        raise Exception(f'problem {problem} not exist!')
    else:
        createTest(problem)