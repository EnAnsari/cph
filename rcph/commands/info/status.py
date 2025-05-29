from rcph.utils.launcher import getInfo, setInfo, checkExistenceProblem
from rcph.utils.tools.color import colored_text
from rcph.config.constant import *

def problemCheck(problem):
    if not checkExistenceProblem(problem):
        raise Exception(f'problem {problem} does not exist!')

def setStatus(problem):
    info = getInfo()
    status = input(colored_text(f'Enter status of problem {problem} (Accept|WA|raw|null): ', 'yellow')).lower()
    
    if status == '':
        return # canceled
    elif status in PROBLEM_STATUS.COMMAND.WRONG_ANSWER:
        status = PROBLEM_STATUS.STATUS.WRONG_ANSWER
    elif status in PROBLEM_STATUS.COMMAND.ACCEPT:
        status = PROBLEM_STATUS.STATUS.ACCEPT
    elif status in PROBLEM_STATUS.COMMAND.RAW:
        status = PROBLEM_STATUS.STATUS.RAW
    elif status in PROBLEM_STATUS.COMMAND.NULL:
        status = PROBLEM_STATUS.STATUS.NULL
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
        

def queraEdit(problem):
    info = getInfo()
    try:
        name = input(colored_text(f'Enter name of problem {problem}: ', 'yellow'))
        percentage = int(input(colored_text('Enter percentage (between 0 and 100): ', 'yellow')))
        if not 0 <= percentage and percentage <= 100:
            raise Exception('your percentage is invalid')
        link = input(colored_text('Enter link of problem: ', 'yellow'))
    except:
        raise Exception(f'your input isn\'t standard!')
    
    for p in info[DICT.PROBLEMS]:
        if p[DICT.LETTER] == problem:
            p[DICT.NAME] = name if name else p[DICT.NAME]
            p[DICT.PERCENTAGE] = percentage
            p[DICT.LINK] = link if link else p[DICT.LINK]

    setInfo(info)