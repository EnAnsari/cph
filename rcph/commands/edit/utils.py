from rcph.config.constant import *
from rcph.utils.launcher import getInfo, setInfo
from rcph.utils.tools.color import colored_text

def inputData(sentence, value):
    data = input(colored_text(f'{sentence}: {value if value != "" else "empty"} (new?): ', 'yellow'))
    if data == '':
        return value
    elif data == '--':
        return ''
    else:
        return data

def editContest():
    print(colored_text('Welcome to contest Editor CLI\n', 'yellow', 'bold'))
    print(colored_text('leave -- if you want change a field to empty', 'blue'))

    info = getInfo()
    
    info[DICT.NAME] = inputData(f'contest name', info[DICT.NAME])
    info[DICT.LINK] = inputData(f'contest link', info[DICT.LINK])
    info[DICT.DETAIL] = inputData(f'contest detail', info[DICT.DETAIL])
    info[DICT.REPO] = inputData(f'contest repository', info[DICT.REPO])
    
    choice = input(colored_text(f'do you want to edit question names ({len(info[DICT.PROBLEMS])} questions - yes/no)? ', 'blue')).lower()
    if choice in ['yes', 'y']:
        for p in info[DICT.PROBLEMS]:
            print(colored_text(f'problem {p[DICT.LETTER]}...', 'magneta'))
            p[DICT.NAME] = inputData('name', p[DICT.NAME])

    setInfo(info)
    print(colored_text('informations successfully updated!', 'green'))