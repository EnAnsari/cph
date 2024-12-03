from rcph.utils.imports import os
from rcph.config.constant import *
from rcph.config.make import makeLocalConfig
from rcph.utils.tools.sign import makeSign
from rcph.utils.launcher import getTemplate, getGlobaltConfig

def checkFolderExistence(folder_path):
    if os.path.exists(folder_path):
        raise FileExistsError(f"Folder already exists: {folder_path}")
    

def makeFolder(folder_path):
    checkFolderExistence(folder_path)
    os.mkdir(folder_path)


def getContestInfo():
    contest = {
        DICT.NAME: '',
        DICT.LINK: '',
        DICT.DETAIL: '',
        DICT.REPO: '',
        DICT.PROBLEMS : [],
    }

    contest[DICT.NAME] = input("Enter Contest Name: ")
    if contest[DICT.NAME] != '':
        contest[DICT.LINK] = input("Enter Contest link: ")
        contest[DICT.LINK] = input("Enter Contest detail: ")
        contest[DICT.REPO] = input("Enter Contest repository: ")

    problems = input('Enter name/numbers of problems: ')

    
    if problems.isdigit():
        for i in range(int(problems)):
            contest[DICT.PROBLEMS].append(chr(ord('a') + i))
    else:
        for name in problems.split():
            contest[DICT.PROBLEMS].append(name)

    return contest

def testCaseMaker(folder_path, contest):
    tc = os.path.join(folder_path, TESTCASE_FOLDER)
    os.mkdir(tc)
    for problem in contest[DICT.PROBLEMS]:
        os.mkdir(os.path.join(tc, problem))


def makeRcphFolder(folder_path, contest, parent):
    rcph_folder = os.path.join(folder_path, RCPH_FOLDER)
    os.mkdir(rcph_folder)
    makeLocalConfig(rcph_folder, folder_path, contest, parent)
    testCaseMaker(rcph_folder, contest)


def makeTemplateCode(folder_path):
    template = getTemplate()
    with open(os.path.join(folder_path, TEMPLATE_CPP), 'w') as template_file:
        template_file.write(template)


def makeProblemScript(folder_path, problem):
    """
    creating problem script
    Args:
        contest folder path
        problem letter
    """
    template = getTemplate()
    config = getGlobaltConfig()
    sign_flag = config[DICT.SIGN]

    with open(os.path.join(folder_path, problem + '.cpp'), 'w') as problem_code:
        if sign_flag:
            if config[DICT.SIGN_DETAIL][DICT.SIDE] == DICT.TOP:
                script =  makeSign(folder_path, problem) + '\n' + template
            else: # bottom
                script = template + '\n' + makeSign(folder_path, problem)
        else:
            script = template

        problem_code.write(script)

def makeProblemCodes(folder_path, contest):
    for problem in contest[DICT.PROBLEMS]:
        makeProblemScript(folder_path, problem)