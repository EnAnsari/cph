from rcph.utils.imports import os, sys, subprocess
from rcph.config.constant import *
from rcph.utils.color import colored_text


def compareText(text1, text2):
    for x, y in zip(text1.split('\n'), text2.split('\n')):
        if x.strip() != y.strip():
            return False
    
    if len(text1.split('\n')) != len(text2.split('\n')):
        return False
    
    return True


def getFolder(problem):
    problem_folder = os.path.join(os.getcwd(), RCPH_FOLDER, TESTCASE_FOLDER, problem)
    if not os.path.exists(problem_folder):
        raise Exception(f'problem {problem} does not exist!')
    return problem_folder


def getExecutiveFile():
    exe = os.path.join(os.getcwd(), "a.exe" if sys.platform == 'win32' else "a.out")
    if not os.path.exists(exe):
        raise Exception("Executable not found! Compile your C++ file.")
    return exe


def execute(exe, input_content):
    proc = subprocess.run([exe], input=input_content, text=True, capture_output=True)
    output = proc.stdout.strip()
    return output

def judge(problem):
    problem_folder = getFolder(problem)
    exe = getExecutiveFile()

    print(colored_text(f'problem {problem.upper()} judgement...', 'cyan', 'bold'))

    t, p = 1, 0  # Test number, passed count
    while os.path.exists(os.path.join(problem_folder, str(t) + '.in')) and os.path.exists(os.path.join(problem_folder, str(t) + '.ans')):
        print(colored_text(f"Running Test {t}...", 'magneta'))
        with open(os.path.join(problem_folder, str(t) + '.in')) as fin, open(os.path.join(problem_folder, str(t) + '.ans')) as fans:
            input_content = fin.read().strip()
            output = execute(exe, input_content)
            expected = fans.read().strip()

            if compareText(output, expected):
                print(f"{colored_text('Input:', 'cyan')}\n{input_content}\n{colored_text('Expected:', 'cyan')}\n{expected}")
                print(colored_text(f"Test {t} PASSED!\n", 'green', 'bold'))
                p += 1
            else: 
                print(f"{colored_text('Input:', 'cyan')}\n{input_content}\n{colored_text('Expected:', 'cyan')}\n{expected}\n{colored_text('Got:', 'cyan')}\n{output}")
                print(colored_text(f"Test {t} FAILED!\n", 'red', 'bold'))
        t += 1

    if t - 1 == 0:
        print(colored_text(f'there is not any test case for problem {problem}', 'yellow'))
    else:
        print(colored_text(f"{p} test(s) passed, {t-p-1} test(s) failed!", 'blue'))
        if t-p-1 == 0:
            print('status:', colored_text('Accept\n', 'green', 'bold'))
        else:
            print('status:', colored_text('Wrong Answer\n', 'red', 'bold'))


def executeInput():
    input_path = os.path.join(os.getcwd(), 'input.txt')
    if not os.path.exists(input_path):
        raise Exception('input.txt file does not exist!')
    with open(input_path, 'r') as fin:
        input_content = fin.read().strip()
    
    exe = getExecutiveFile()
    output = execute(exe, input_content)
    
    with open(os.path.join(os.getcwd(), 'output.txt'), 'w') as fout:
        fout.write(output.strip())