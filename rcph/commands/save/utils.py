from rcph.utils.imports import os, sys
from rcph.utils.launcher import getGlobaltConfig, getConnectionFile
from rcph.utils.tools.color import colored_text
from rcph.utils.tools.clear import clear_terminal
from rcph.config.constant import *
from rcph.commands.asset.utils import advancedListDIR, prompt, prompt_toolkit, DirectoryCompleter, Style, InMemoryHistory
from prompt_toolkit.key_binding import KeyBindings

def checkExistence(file):
    file_path = os.path.join(os.getcwd(), file)
    if not os.path.exists(file_path):
        raise Exception(f'{file} file does not exist!')
    return file_path

def explore():
    config = getGlobaltConfig()
    hidden_items = config[COMMANDS.HIDDEN_ITEMS]
    connection = getConnectionFile()

    
    dir = os.path.join(connection[ASSET_FOLDER], SAVED)
    os.makedirs(dir, exist_ok=True)
    curr, curr_show = dir, ''

    def getCWD():
        return curr
    
    completer = DirectoryCompleter(getCWD, hidden_items)
    history = InMemoryHistory()
    style = Style.from_dict({
        'prompt': 'ansigreen bold',  # Green color for the prompt
        '': 'ansiblack',             # Default color for the input text
    })
    bindings = KeyBindings()

    exitCondition = False

    @bindings.add('c-s')
    def _(event):
        print("\nCtrl+S detected! Exiting the loop...")
        exitCondition = True
        event.app.exit()
    
    while not exitCondition:
        try:
            user_input = prompt(f"{curr_show}> ", completer=completer, style=style, history=history).strip()
            path = os.path.join(curr, *user_input.split('/'))

            # handle save command
            if user_input.lower() == 'save':
                return path

            # handle empty input
            elif user_input == '':
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
                print(colored_text('this is not a directory! pls select one of them...', 'red'))
            
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
        
    return path

def fileSaving(src, des):
    pass