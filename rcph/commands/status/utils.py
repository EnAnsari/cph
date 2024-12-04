from rcph.utils.imports import os
from rcph.utils.launcher import getInfo, setInfo
from rcph.utils.tools.color import colored_text
from rcph.config.constant import *


def checkExistenceProblem(problem):
    info = getInfo()
    for p in info[DICT.PROBLEMS]:
        if p[DICT.LETTER] == problem:
            return True
    # return False # problem does not exist!
    raise Exception(f'problem {problem} does not exist!')


def setStatus(problem):
    info = getInfo()
    status = input(colored_text(f'Enter status of problem {problem} (Accept|WA|raw|null): ', 'yellow')).lower()
    
    if status == '':
        return # canceled
    elif status in ['wrong answer', 'wa',  'wrong']:
        status = 'Wrong Answer'
    elif status in ['accept', 'correct', 'acc']:
        status = 'Accept'
    elif status == 'raw':
        status = 'raw'
    elif status in ['null', 'none']:
        status = 'null'
    else:
        raise Exception(f'{status} is invalid for status!')
    
    for p in info[DICT.PROBLEMS]:
        if p[DICT.LETTER] == problem:
            p[DICT.STATUS] = status
    setInfo(info)
    

def setMultiStatus():
    info = getInfo()
    for p in info[DICT.PROBLEMS]:
        print(colored_text(f'problem {p[DICT.LETTER]} status was: {p[DICT.STATUS]}...', 'magneta'))
        setStatus(p[DICT.LETTER])