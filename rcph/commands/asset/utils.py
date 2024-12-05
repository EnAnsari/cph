from rcph.utils.imports import os, shutil, prompt_toolkit, sys
from rcph.utils.launcher import setAssetConnection, getAssetDirectory, getGlobaltConfig
from rcph.utils.tools.color import colored_text
from rcph.utils.tools.clear import clear_terminal
from rcph.config.constant import *

from prompt_toolkit import prompt
from prompt_toolkit.completion import Completer, Completion
from prompt_toolkit.styles import Style
from prompt_toolkit.history import InMemoryHistory


class DirectoryCompleter(Completer):
    def __init__(self, get_cwd, hidden_items):
        self.get_cwd = get_cwd
        self.hidden_items = hidden_items

    def get_completions(self, document, complete_event):
        text = document.text
        dir = text.split('/')[:-1]
        text = text.split('/')[-1]
        try:
            items = os.listdir(os.path.join(self.get_cwd(), *dir))
            if not self.hidden_items:
                items = [item for item in items if not item.startswith('.')]
            items.sort()
        except PermissionError:
            items = []
        
        for item in items:
            if item.startswith(text):
                if os.path.isdir(os.path.join(self.get_cwd(), item)):
                    yield Completion(item, start_position=-len(text), style='fg:ansiblue bold')
                else:
                    yield Completion(item, start_position=-len(text), style='fg:ansiyellow')


def explore(dir):
    config = getGlobaltConfig()
    hidden_items = config[COMMANDS.HIDDEN_ITEMS]
    curr, curr_show = dir, ''

    def getCWD():
        return curr
    
    completer = DirectoryCompleter(getCWD, hidden_items)
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
                    advancedListDIR(curr, hidden_items)

            # handle ls command
            elif user_input.lower() == "ls":
                advancedListDIR(curr, hidden_items)
            
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

def advancedListDIR(curr, hidden_items):
    try:
        items = os.listdir(curr)
        
        if not items:
            print(colored_text("No files or directories in this directory.", 'red'))

        if not hidden_items:
            items = [item for item in items if not item.startswith('.')]
        items.sort()

        dirs = []
        files = []

        for item in items:
            item_path = os.path.join(curr, item)
            if os.path.isdir(item_path):
                dirs.append(item)
            else:
                files.append(item)
        
        for dir in dirs:
            print(colored_text(f"./{dir}", 'blue'))
        
        for file in files:
            if file.endswith('.h'):
                print(colored_text(file, 'yellow'))
            elif file.endswith('.cpp'):
                splitted = file.split('.')
                if 'func' in splitted:
                    print(colored_text(file, 'magneta'))
                elif 'stl' in splitted:
                    print(colored_text(file, 'green'))
                else:
                    print(file)
            else:
                print(colored_text(file, 'black'))
    except PermissionError:
        print("Permission denied!")


def makeConnection():
    setAssetConnection(os.getcwd())

def getAssetFile():
    dir = getAssetDirectory()
    if not dir:
        raise Exception('asset directory is empty! please connect someone!')
    
    file_path = explore(dir)
    des = input(colored_text('Enter destination file: ', 'yellow'))
    if des == '':
        des = os.path.basename(file_path)
    
    des_path = os.path.join(os.getcwd(), ASSET_FOLDER, *des.split('/')[:-1])
    os.makedirs(des_path, exist_ok=True)

    des_path = os.path.join(des_path, des.split('/')[-1])
    shutil.copy(file_path, des_path)
    print(colored_text('asset successfully copied!', 'green'))