from rcph.config.constant import *
from rcph.utils.imports import os
from rcph.utils.launcher import getInfo, setInfo
from rcph.utils.tools.color import colored_text
from rcph.commands.init.utils import makeProblemScript

def checkProblemExist(info, problem_letter):
    for problem in info[DICT.PROBLEMS]:
        if problem_letter == problem[DICT.LETTER]:
            return True
    return False # problem doesn't exist!

def addProblem(problem):
    info = getInfo()
    if checkProblemExist(info, problem):
        print(colored_text(f'problem {problem} exist before!', 'red'))
        return

    info[DICT.PROBLEMS].append({
        DICT.LETTER: problem,
        DICT.NAME: '',
        DICT.STATUS: DICT.NULL
    })
    setInfo(info)
    makeProblemScript(os.getcwd(), problem)
    os.mkdir(os.path.join(os.getcwd(), RCPH_FOLDER, TESTCASE_FOLDER, problem))
    print(colored_text(f'problem {problem} successfully added!', 'green'))


def addMultiProblems():
    problems = input(colored_text('Enter problems name to add: ', 'yellow')).split()
    for problem in problems:
        addProblem(problem)
