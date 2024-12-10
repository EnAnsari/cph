from rcph.utils.imports import os, shutil, prompt_toolkit, sys, pathlib
from rcph.utils.launcher import setConnection, getAssetDirectory, getGlobaltConfig, getConnection, getAssetShortcuts
from rcph.utils.tools.color import colored_text
from rcph.utils.tools.clear import clear_terminal
from rcph.config.constant import *

from prompt_toolkit import prompt
from prompt_toolkit.styles import Style
from prompt_toolkit.history import InMemoryHistory

from .utils import DirectoryCompleter, advancedListDIR

def makeConnection():
    connection = getConnection()
    connection['asset'] = os.getcwd()
    setConnection(connection)

def explore(dir):
    config = getGlobaltConfig()
    hidden_items = config[COMMANDS.HIDDEN_ITEMS]
    shortcut = getAssetShortcuts()
    curr, curr_show = dir, ''

    def getCWD():
        return curr
    
    completer = DirectoryCompleter(getCWD, hidden_items, shortcut)
    history = InMemoryHistory()
    style = Style.from_dict({
        'prompt': 'ansigreen bold',  # Green color for the prompt
        '': 'ansiblack',             # Default color for the input text
    })
    
    while True:
        try:
            user_input = prompt(f"{curr_show}> ", completer=completer, style=style, history=history).strip()
            path = os.path.join(curr, *user_input.split('/'))

            # handle empty input
            if user_input == '':
                if config[COMMANDS.LS_BY_ENTER]:
                    advancedListDIR(curr, hidden_items, shortcut)

            # handle ls command
            elif user_input.lower() == "ls":
                advancedListDIR(curr, hidden_items, shortcut)
            
            # handle clear command
            elif user_input.lower() == 'clear':
                clear_terminal()
            
            # handle ..* command
            elif all(char == '.' for char in user_input):
                for _ in range(len(user_input) - 1): # for each extra . after .. we are back one directory
                    if curr != dir:
                        curr = os.path.dirname(curr)                   
                        curr_show = os.path.dirname(curr_show)
            
            # handle ~ command
            elif user_input == '~':
                curr, curr_show = dir, ''
            
            # handle exit command
            elif user_input.lower() == 'exit':
                sys.exit(0)

            # handle navigation into subdirectories
            elif os.path.isdir(path):
                curr = path
                curr_show = os.path.join(curr_show, user_input)
                while True:
                    if curr in shortcut:
                        listdir = shortcut[curr]
                    else:
                        listdir = os.listdir(curr)
                    if len(listdir) == 1 and os.path.isdir(os.path.join(curr, listdir[0])):
                        curr = os.path.join(curr, listdir[0])
                        curr_show = os.path.join(curr_show, listdir[0])
                    else:
                        break

            # handle file selection
            elif os.path.isfile(path):
                return path
            
            # handle invalid commands
            else:
                print(colored_text('invalid command!', 'red'))

        # Graceful exit on Ctrl+C
        except KeyboardInterrupt:
            print(colored_text('bye bye!','yellow'))
            sys.exit(0)

        # Catch unexpected errors
        except Exception as e:
            raise Exception(f'We have some Error: {e}')



def getAssetFile():
    dir = getAssetDirectory()
    if not dir:
        raise Exception('asset directory is empty! please connect someone!')
    
    file_path = explore(dir)
    des = input(colored_text('Enter destination file: ', 'yellow'))
    if des == '':
        des = os.path.basename(file_path)
    
    des_path = pathlib.Path(os.path.join(os.getcwd(), DATA.ASSET_FOLDER, *des.split('/')[:-1])).resolve()
    print(des_path)
    os.makedirs(des_path, exist_ok=True)

    des_path = os.path.join(des_path, des.split('/')[-1])
    shutil.copy(file_path, des_path)
    print(colored_text('asset successfully copied!', 'green'))