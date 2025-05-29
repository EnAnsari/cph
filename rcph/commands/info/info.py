from rcph.config.constant import *
from rcph.utils.launcher import getInfo, testCounter
from rcph.utils.tools.color import colored_text

def showSentence(sentence, value):
    print(
        colored_text(sentence, 'blue'),
        colored_text(value, 'cyan', 'bold') if value else colored_text('-empty-', 'yellow')
    )

def showStatus(status):
    if status == 'Accept':
        color = 'green'
    elif status == 'Wrong Answer':
        color = 'red'
    elif status == 'raw':
        color = 'cyan'
    else:
        color = 'yellow'
    
    return colored_text(status, color, 'bold')

def showPercentage(percentage):
    if percentage == 0:
        color = 'red'
    elif percentage == 100:
        color = 'green'
    else:
        color = 'yellow'
    return f"{colored_text(percentage, color, 'bold')}%"

def showProblemInfo(problem):
    print(
        colored_text(problem[DICT.LETTER].upper(), 'yellow'), '\t',
        colored_text(problem[DICT.NAME], 'blue') if problem[DICT.NAME] else colored_text('-no name-', 'yellow'), '\t',
        colored_text(f'tc num: {testCounter(problem[DICT.LETTER])}', 'cyan'), '\t',
        'status:', showStatus(problem[DICT.STATUS]), '\t',
        showPercentage(problem[DICT.PERCENTAGE]),
        f'{colored_text(problem[DICT.LINK], "blue")}' if problem[DICT.LINK] else ''
    )

def showInfo(info_arg=None):
    info = info_arg or getInfo()

    print(colored_text('About Contest CLI', 'yellow', 'bold'))

    showSentence('contest name:', info[DICT.NAME])
    showSentence('contest link:', info[DICT.LINK])
    showSentence('contest detail:', info[DICT.DETAIL])
    showSentence('contest repo:', info[DICT.REPO])
    print(colored_text('contest parent:', 'blue'), colored_text(info[DICT.PARENT], 'cyan', 'bold'))
    print(colored_text('contest path:', 'blue'), colored_text(info[DICT.PATH], 'cyan', 'bold'))
    
    for problem in info[DICT.PROBLEMS]:
        showProblemInfo(problem)