from rcph.config.constant import *
from rcph.utils.imports import os, shutil
from rcph.utils.launcher import getInfo, setInfo
from rcph.utils.tools.color import colored_text
from rcph.commands.addq.handler import checkProblemExist


def delProblem(problem):
    info = getInfo()
    if not checkProblemExist(info, problem):
        print(colored_text(f'problem {problem} does not exist!', 'red'))
        return

    info[DICT.PROBLEMS] = [p for p in info[DICT.PROBLEMS] if p[DICT.LETTER] != problem]
    setInfo(info)
    
    problem_script = os.path.join(os.getcwd(), problem + '.cpp')
    if os.path.exists(problem_script):
        os.remove(problem_script)
    else:
        print(colored_text(f'problem {problem} has not script file (.cpp)', 'red'))
    
    shutil.rmtree(os.path.join(os.getcwd(), RCPH_FOLDER, TESTCASE_FOLDER, problem))
    print(colored_text(f'problem {problem} successfully deleted!', 'green'))


def delMultiProblems():
    problems = input(colored_text('Enter problems name to delete: ', 'yellow')).split()
    for problem in problems:
        delProblem(problem)