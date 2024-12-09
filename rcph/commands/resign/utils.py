from rcph.utils.imports import os
from rcph.utils.launcher import getInfo
from rcph.utils.tools.script import getProblemScript
from rcph.config.constant import *
from rcph.utils.tools.color import colored_text

def resignProblem(problem):
    problem_path = os.path.join(os.getcwd(), problem + '.cpp')
    with open(problem_path, 'r') as f:
        content = f.readlines()

    script = ''
    ignore = False
    for line in content:
        if line.strip().startswith('/*'):
            ignore = True
        elif line.strip().endswith('*/'):
            ignore = False
        elif not ignore:
            script += line
    new_script = getProblemScript(os.getcwd(), problem, script.strip())
    with open(problem_path, 'w') as f:
        f.write(new_script)
    
    print(colored_text(f'problelm {problem.upper()} resigned successfully!', 'green'))

def multiResign():
    info = getInfo()
    for p in info[DICT.PROBLEMS]:
        resignProblem(p[DICT.LETTER])