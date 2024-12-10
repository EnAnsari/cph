from rcph.utils.imports import os, sys, shutil
from rcph.utils.launcher import getGlobaltConfig, getConnection
from rcph.utils.tools.color import colored_text
from rcph.utils.tools.clear import clear_terminal
from rcph.config.constant import *
from .utils import DirectoryCompleter, advancedListDIR
from .launch import InMemoryHistory, Style, prompt

def checkExistence(file):
    file_path = os.path.join(os.getcwd(), file)
    if not os.path.exists(file_path):
        raise Exception(f'{file} file does not exist!')
    return file_path


def explore():
    print(colored_text('you can use this commands: save, mkdir, rmdir, rm, ls, clear, and direcotry name to enter', 'yellow'))
    config = getGlobaltConfig()
    hidden_items = config[COMMANDS.HIDDEN_ITEMS]
    connection = getConnection()
    
    dir = os.path.join(connection[DATA.ASSET_FOLDER], DATA.SAVED)
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
    
    while True:
        try:
            user_input = prompt(f"{curr_show}> ", completer=completer, style=style, history=history).strip()
            path = os.path.join(curr, *user_input.split('/'))

            # handle save command
            if user_input.lower() == 'save':
                return curr

            # handle empty input
            elif user_input == '':
                if config[COMMANDS.LS_BY_ENTER]:
                    advancedListDIR(curr, hidden_items)

            # handle 'mkdir' command for creating directory
            elif user_input.lower().startswith('mkdir '):
                dir_name = user_input[6:].strip()
                try:
                    os.mkdir(os.path.join(curr, dir_name))
                    print(colored_text(f'{dir_name} successfully created!', 'green'))
                except FileExistsError:
                    print(colored_text(f'Error: directory {dir_name} already exist!', 'red'))

            # handle 'rmdir' command for deleting empty directories
            elif user_input.lower().startswith('rmdir '):
                dir_name = user_input[6:].strip()
                dir_path = os.path.join(curr, dir_name)
                if os.path.isdir(dir_path):
                    if not os.listdir(dir_path):
                        os.rmdir(dir_path)
                        print(colored_text(f'{dir_name} successfully removed!', 'green'))
                    else:
                        print(colored_text(f'{dir_name} is not empty!', 'red'))
                else:
                    print(colored_text(f'{dir_name} is not exist!', 'red'))

            # handle 'rm' command for deleting files
            elif user_input.lower().startswith('rm '):
                file_name = user_input[3:].strip()
                file_path = os.path.join(curr, file_name)
                if os.path.isfile(file_path):
                    os.remove(file_path)
                    print(colored_text(f'{file_name} successfully removed!', 'green'))
                else:
                    print(colored_text(f'{file_name} is not a file!', 'red'))

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


def fileSaving(src, des):
    file_saved_name = input(colored_text('Enter your file name to save: ', 'yellow'))
    if file_saved_name == '':
        file_saved_name = os.path.basename(src)
    
    des_path = os.path.join(des, file_saved_name)
    if os.path.exists(des_path):
        print(colored_text(f'{file_saved_name} exist in this directory, please try another name!', 'red'))
        return fileSaving(src, des)
    
    shutil.copy(src, des_path)
    print(colored_text('your file successfully saved!', 'green'))