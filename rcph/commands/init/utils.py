from rcph.utils.imports import os, shutil, json
from rcph.config.constant import *
from rcph.config.make import makeLocalConfig
from rcph.utils.tools.sign import makeSign
from rcph.utils.launcher import getTemplate, getGlobaltConfig

def makeFolder(folder_path):
    if not os.path.exists(folder_path):
        os.mkdir(folder_path)
    else:
        raise FileExistsError(f"Folder already exists: {folder_path}")


def getContestInfo():
    contest = {
        'name': '',
        'link': '',
        'detail': '',
        'repo': '',
        'problems' : [],
    }

    contest['name'] = input("Enter Contest Name: ")
    if contest['name'] != '':
        contest['link'] = input("Enter Contest link: ")
        contest['detail'] = input("Enter Contest detail: ")
        contest['repo'] = input("Enter Contest repository: ")

    problems = input('Enter name/numbers of problems: ')

    
    if problems.isdigit():
        for i in range(int(problems)):
            contest['problems'].append(chr(ord('a') + i))
    else:
        for name in problems.split():
            contest['problems'].append(name)

    return contest


def testCaseMaker(folder_path, contest):
    tc = os.path.join(folder_path, TESTCASE_FOLDER)
    os.mkdir(tc)
    for problem in contest['problems']:
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


def makeProblemCodes(folder_path, contest):
    template = getTemplate()
    config = getGlobaltConfig()
    sign_flag = config['sign']

    for problem in contest['problems']:
        with open(os.path.join(folder_path, problem + '.cpp'), 'w') as problem_code:
            if sign_flag:
                problem_code.write(makeSign(folder_path, problem))
            problem_code.write(template)