from rcph.utils import os, shutil, json
from rcph.config.constant import *
from rcph.config.make import run as makeCofingJson
from rcph.utils.sign import makeSign
from rcph.utils.get import getTemplate, getGlobaltConfig

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
    makeCofingJson(rcph_folder, folder_path, contest, parent)
    testCaseMaker(rcph_folder, contest)


def makeTemplateCode(folder_path):
    template = getTemplate()
    shutil.copy(template, os.path.join(folder_path, TEMPLATE_CPP))


def makeProblemCodes(folder_path, contest):
    template = getTemplate()

    with open(template, 'r') as template_file:
        template = template_file.read()

    config = getGlobaltConfig()
    sign_flag = config['sign']

    for problem in contest['problems']:
        with open(os.path.join(folder_path, problem + '.cpp'), 'w') as problem_code:
            if sign_flag:
                problem_code.write(makeSign(folder_path, problem))
            problem_code.write(template)

def addToDB(folder_path):
    here = os.path.dirname(__file__)
    contestDB_path = os.path.join(here, *['..'] * 3, COMPONENTS, DB_FOLDER, CONTEST_DB_NAME)

    if os.path.exists(contestDB_path):
        with open(contestDB_path, 'r') as contestDB_file:
            contestDB = json.load(contestDB_file)
    else:
        contestDB = []

    contestDB.append(folder_path)
    with open(contestDB_path, 'w') as contestDB_file:
        json.dump(contestDB, contestDB_file, indent=4)