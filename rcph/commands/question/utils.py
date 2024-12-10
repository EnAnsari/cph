from rcph.config.constant import *
from rcph.utils.imports import os, shutil
from rcph.utils.launcher import getInfo, setInfo, checkExistenceProblem
from rcph.utils.tools.script import getProblemScript
from rcph.utils.tools.color import colored_text

def addProblem(problem):
    info = getInfo()

    info[DICT.PROBLEMS].append({
        DICT.LETTER: problem,
        DICT.NAME: '',
        DICT.STATUS: DICT.NULL
    })
    setInfo(info)
    with open(os.path.join(os.getcwd(), problem + '.cpp'), 'w') as problem_code:
        problem_code.write(getProblemScript(os.getcwd(), problem))
    os.mkdir(os.path.join(os.getcwd(), CURRENT.RCPH_FOLDER, CURRENT.TESTCASE_FOLDER, problem))
    print(colored_text(f'problem {problem} successfully added!', 'green'))


def addProblemByCheck(problem):
    if checkExistenceProblem(problem):
        print(colored_text(f'problem {problem} exist before!', 'red'))
    else:
        addProblem(problem)


def addMultiProblems():
    problems = input(colored_text('Enter problems name/num to add (maybe a..d): ', 'yellow'))
    if problems.isdigit():
        for i in range(int(problems)):
            problem_letter = chr(ord('a') + i)
            addProblemByCheck(problem_letter)
    elif len(problems) == 4 and problems[1:3] == '..':
        problem_letter = problems[0].lower()
        while True:
            addProblemByCheck(problem_letter)
            if problem_letter == problems[3].lower():
                break
            problem_letter = chr(ord(problem_letter) + 1)
    else:
        for problem_letter in problems.split():
            addProblemByCheck(problem_letter)


def delProblemByCheck(problem):
    if not checkExistenceProblem(problem):
        print(colored_text(f'problem {problem} does not exist!', 'red'))
    else:
        delProblem(problem)


def delProblem(problem):
    info = getInfo()

    info[DICT.PROBLEMS] = [p for p in info[DICT.PROBLEMS] if p[DICT.LETTER] != problem]
    setInfo(info)
    
    problem_script = os.path.join(os.getcwd(), problem + '.cpp')
    if os.path.exists(problem_script):
        os.remove(problem_script)
    else:
        print(colored_text(f'problem {problem} has not script file ({problem}.cpp)', 'red'))
    
    shutil.rmtree(os.path.join(os.getcwd(), CURRENT.RCPH_FOLDER, CURRENT.TESTCASE_FOLDER, problem))
    print(colored_text(f'problem {problem} successfully deleted!', 'green'))


def delMultiProblems():
    problems = input(colored_text('Enter problems name to delete (maybe a..d | ALL): ', 'yellow'))
    if problems == 'ALL':
        for problem in getInfo()[DICT.PROBLEMS]:
            delProblem(problem[DICT.LETTER])
    elif len(problems) == 4 and problems[1:3] == '..':
        problem_letter = problems[0].lower()
        while True:
            delProblemByCheck(problem_letter)
            if problem_letter == problems[3].lower():
                break
            problem_letter = chr(ord(problem_letter) + 1)
    else:
        for problem_letter in problems.split():
            delProblemByCheck(problem_letter)