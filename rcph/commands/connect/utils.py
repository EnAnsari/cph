from rcph.utils.imports import os
from rcph.utils.launcher import getConnection, setConnection
from rcph.config.constant import *
from rcph.utils.tools.color import colored_text

def makeConnection(file):
    path = os.path.join(os.getcwd(), file if file else '').replace('\\', '/') # replace for windows platform
    if not os.path.exists(path):
        raise Exception(f'this path doesn\'t exist!')
    choices = [DATA.ASSET_FOLDER, DATA.TCBANK, DATA.CHROMEDRIVER]
    for i, ch in enumerate(choices):
        print(colored_text(f'[{i + 1}]', 'yellow'), colored_text(ch, 'green'))
    choice = input(colored_text('Enter your choice: ', 'blue'))
    if not choice.isdigit() or int(choice) < 1 or int(choice) > len(choices):
        raise Exception('invalid input!')
    
    choice = int(choice) - 1

    connection = getConnection()
    connection[choices[choice]] = path
    setConnection(connection)
    print(colored_text(f'{path} connected as {choices[choice]} successfully!', 'green'))