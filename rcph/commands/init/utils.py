from rcph.utils.imports import os
from rcph.config.constant import *
from rcph.config.make import makeLocalConfig
from rcph.utils.tools.color import colored_text
from rcph.utils.tools.script import getProblemScript
from rcph.utils.launcher import getTemplate, isDevMode, currentIsContest, setInfo, getContestDB, setContestDB

def getProblems():
    problems_input = input(colored_text('Enter name/numbers of problems: ', 'yellow'))

    problems = []
    if problems_input.isdigit():
        for i in range(int(problems_input)):
            problems.append(chr(ord('a') + i))
    else:
        for name in problems_input.split():
            problems.append(name)
    
    return problems

def testCaseMaker(folder_path, problems):
    tc = os.path.join(folder_path, CURRENT.TESTCASE_FOLDER)
    os.mkdir(tc)
    for problem in problems:
        os.mkdir(os.path.join(tc, problem))

def makeRcphFolder(folder_path, contest_link, parent, problems):
    rcph_folder = os.path.join(folder_path, CURRENT.RCPH_FOLDER)
    os.mkdir(rcph_folder)
    info = makeLocalConfig(folder_path, contest_link, parent, problems)
    setInfo(info, folder_path)
    testCaseMaker(rcph_folder, problems)

def makeTemplateCode(folder_path):
    template = getTemplate()
    with open(os.path.join(folder_path, CURRENT.TEMPLATE_CPP), 'w') as template_file:
        template_file.write(template)

def makeProblemScript(folder_path, problem_letter):
    with open(os.path.join(folder_path, problem_letter + '.cpp'), 'w') as problem_code:
        problem_code.write(getProblemScript(folder_path, problem_letter))

def makeProblemCodes(folder_path, problems):
    for problem in problems:
        makeProblemScript(folder_path, problem)

def commonContestMakerTasks(folder_path, parent, test, problems=[]):
    contest_link = input(colored_text("Enter Contest link: ", 'yellow'))
    makeRcphFolder(folder_path, contest_link, parent, problems)
    if not isDevMode() and not test:
        db = getContestDB()
        db.append(folder_path)
        setContestDB(db)

def createContestInFolder(folder_path, parent, test):
    if currentIsContest(folder_path):
        raise Exception(f'a contest exist before!')
    commonContestMakerTasks(folder_path, parent, test)
    print(f'\nyour contest created {colored_text("successfully", "green", "bold")}!')

def createContestByFolder(folder_name, parent, test):
    folder_path = os.path.join(os.getcwd(), folder_name).replace('\\', '/') # replace for windows platform
    if os.path.exists(folder_path):
        raise Exception(f'{folder_name} was exist before!')
    problems = getProblems()
    os.mkdir(folder_path)
    commonContestMakerTasks(folder_path, parent, test, problems)
    makeTemplateCode(folder_path)
    makeProblemCodes(folder_path, problems)
    print(f'please run this command to enter your contest directory:')
    print(colored_text(f'cd ./{folder_name}', 'yellow', 'bold'))