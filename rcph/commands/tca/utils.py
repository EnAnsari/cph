from rcph.utils.imports import os, zipfile
from rcph.config.constant import *
from rcph.utils.launcher import getInfo, testCounter
from rcph.utils.tools.color import colored_text


def clearTestCasesOfProblem(folder):
    num = 0
    for item in os.listdir(folder):
        item_path = os.path.join(folder, item)
        if os.path.isfile(item_path):
            os.remove(item_path)
            num += 1
    print(colored_text(f'{num} file was deleted!', 'red'))


def clearTestCases():
    info = getInfo()
    tc_folder = os.path.join(os.getcwd(), CURRENT.RCPH_FOLDER, CURRENT.TESTCASE_FOLDER)
    for problem in info[DICT.PROBLEMS]:
        problem_tc = os.path.join(tc_folder, problem[DICT.LETTER])
        if os.path.exists(problem_tc):
            clearTestCasesOfProblem(problem_tc)


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
    if in_f == '':
        return

    print(colored_text('Enter output:', 'cyan'))
    out_f = textInput()
    if out_f == '':
        return

    with open(os.path.join(folder, num + '.in'), 'w') as ifile, open(os.path.join(folder, num + '.ans'), 'w') as ofile:
        ifile.write(in_f)
        ofile.write(out_f)


def createTest(problem):
    problemFolder = os.path.join(os.getcwd(), CURRENT.RCPH_FOLDER, CURRENT.TESTCASE_FOLDER, problem)
    testNum = testCounter(problem)
    num = input(colored_text(f'Availabe test(s): {testNum}, how many to add? ', 'yellow'))
    
    if num in COMMANDS.CLEAR:
        clearTestCasesOfProblem(problemFolder)

    num = int(num) if num.isdigit() else 0
    for i in range(num):
        print(colored_text(f'Test case number {i + 1 + testNum}...', 'blue'))
        addTestcase(problemFolder, str(i + 1 + testNum))


def totalAdding():
    tc = os.path.join(os.getcwd(), CURRENT.RCPH_FOLDER, CURRENT.TESTCASE_FOLDER)
    entries = os.listdir(tc)
    folders = [entry for entry in entries if os.path.isdir(os.path.join(tc, entry))]
    folders.sort()
    for problem in folders:
        print(colored_text(f'Problem {problem}...', 'magneta'))
        createTest(problem)

# copy and paste sample zip files in tc folder
def domjudge():
    tc = os.path.join(os.getcwd(), CURRENT.RCPH_FOLDER, CURRENT.TESTCASE_FOLDER)
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