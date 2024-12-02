from rcph.utils.imports import os, zipfile
from rcph.config.constant import *
from rcph.utils.launcher import getInfo, setInfo
from rcph.utils.color import colored_text


def updateInfoTestCase(problem):
    info = getInfo()
    for p in info['problems']:
        if problem == p['letter']:
            p['test case'] = 1
            break
    setInfo(info)

def testCounter(problemFolder):
    result = 1
    while os.path.exists(os.path.join(problemFolder, str(result) + '.in')) and os.path.exists(os.path.join(problemFolder, str(result) + '.ans')):
        result += 1
    return result - 1


def textInput():
    lines = []
    while True:
        line = input()
        if line.strip() == "":
            break
        lines.append(line)
    return '\n'.join(lines)


def addTestcase(folder, num):
    print(colored_text('Enter input:', 'cyan'))
    in_f = textInput()
    print(colored_text('Enter output:', 'cyan'))
    out_f = textInput()
    with open(os.path.join(folder, num + '.in'), 'w') as ifile, open(os.path.join(folder, num + '.ans'), 'w') as ofile:
        ifile.write(in_f)
        ofile.write(out_f)


def createTest(problem):
    problemFolder = os.path.join(os.getcwd(), RCPH_FOLDER, TESTCASE_FOLDER, problem)
    if not os.path.exists(problemFolder):
        raise f'problem {problem} not found!'
    testNum = testCounter(problemFolder)
    num = input(colored_text(f'Availabe test(s): {testNum}, how many to add? ', 'yellow'))
    num = int(num) if num.isdigit() else 0
    for i in range(num):
        print(colored_text(f'Test case number {i + 1 + testNum}...', 'blue'))
        addTestcase(problemFolder, str(i + 1 + testNum))

    if num != 0:
        updateInfoTestCase(problem)


def totalAdding():
    tc = os.path.join(os.getcwd(), RCPH_FOLDER, TESTCASE_FOLDER)
    entries = os.listdir(tc)
    folders = [entry for entry in entries if os.path.isdir(os.path.join(tc, entry))]
    folders.sort()
    for problem in folders:
        print(colored_text(f'Problem {problem}...', 'magneta'))
        createTest(problem)


def domjudge():
    tc = os.path.join(os.getcwd(), RCPH_FOLDER, TESTCASE_FOLDER)
    files = os.listdir(tc)
    for file in files:
        if file.endswith('.zip'):
            name = os.path.splitext(file)[0].replace('samples-', '').lower()
            target_folder = os.path.join(tc, name)
            file_address = os.path.join(tc, file)
            # os.makedirs(target_folder, exist_ok=True) # we have folder before
            with zipfile.ZipFile(file_address, 'r') as zip_ref:
                zip_ref.extractall(target_folder)
            os.remove(file_address)
            updateInfoTestCase(name)