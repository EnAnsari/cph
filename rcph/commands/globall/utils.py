from rcph.utils.imports import os, sys, subprocess, shutil, Completer, Completion, prompt, Style, InMemoryHistory
from rcph.utils.tools.color import colored_text
from rcph.utils.tools.clear import clear_terminal
from rcph.utils.launcher import getContestDB, getInfo
from rcph.config.constant import *
from rcph.commands.info.info import showInfo

def _makeDB():
    db = getContestDB()
    contest_dict = {}
    for contest in db:
        if not os.path.exists(contest):
            print(colored_text(f'contest by path {contest} not exist!', 'red'))
            continue
        contest_info = getInfo(contest)
        if contest_info[DICT.PARENT] in contest_dict:
            contest_dict[contest_info[DICT.PARENT]][0].append(contest_info[DICT.NAME])
            contest_dict[contest_info[DICT.PARENT]][1].append(contest_info[DICT.PATH])
        else:
            contest_dict[contest_info[DICT.PARENT]] = [[contest_info[DICT.NAME]], [contest_info[DICT.PATH]]]
    
    return contest_dict

class DirectoryCompleter(Completer):
    def __init__(self, db, getParent):
        self.db = db
        self.getParent = getParent

    def get_completions(self, document, complete_event):
        text = document.text
        parent = self.getParent()
        if parent:
            items = self.db[parent][0]
        else:
            items = list(self.db.keys())
    
        for item in items:
            if item.startswith(text):
                if parent:
                    yield Completion(item, start_position=-len(text), style='fg:ansiblue bold')
                else:
                    yield Completion(item, start_position=-len(text), style='fg:ansiyellow')

def contestList(contest_list):
    for contest in contest_list[1]:
        conntest_info = getInfo(contest)
        message = colored_text(conntest_info[DICT.NAME], 'cyan') + ' ('
        message += colored_text(conntest_info[DICT.DETAIL], 'yellow') + ' ' if conntest_info[DICT.DETAIL] else ''
        message += colored_text(f'by {len(conntest_info[DICT.PROBLEMS])} problem)', 'green')
        print(message)

def openCode(folder_path):
    try:
        if not os.path.isdir(folder_path):
            print(colored_text(f"The folder '{folder_path}' does not exist!", 'red'))
        else:
            if sys.platform == 'win32':
                subprocess.Popen(["code", folder_path], shell=True)
            else:
                subprocess.run(["code", folder_path], check=True)
            print(colored_text(f"Opened '{folder_path}' in VS Code successfully!", 'green'))
    except FileNotFoundError as e:
        print(colored_text(f'file not found: {e}', 'red'))
    except subprocess.CalledProcessError as e:
        print(colored_text(f"Failed to open VS Code: {e}"), 'red')
    except Exception as e:
        print(colored_text(f"An unexpected error occurred: {e}", 'red'))

def copyContest(folder_path, folder_name='global'):
    try:
        shutil.copytree(folder_path, os.path.join(os.getcwd(), folder_name, os.path.basename(folder_path)))
        print(colored_text(f"Folder copied successfully!", 'green'))
    except FileExistsError:
        print(colored_text(f"The destination folder already exists!", 'red'))
    except Exception as e:
        print(colored_text(f"An error occurred: {e}", 'red'))

def getAddress(db, user_input):
    for i in range(len(db[0])):
        if user_input == db[0][i]:
            return db[1][i]
    return None

def explore():
    db = _makeDB()
    history = InMemoryHistory()
    style = Style.from_dict({
        'prompt': 'ansigreen bold',  # Green color for the prompt
        '': 'ansiblack',             # Default color for the input text
    })
    
    parent = None
    def getParent():
        return parent
    completer = DirectoryCompleter(db, getParent)

    while True:
        try:
            user_input = prompt(f"{parent if parent else ''}> ", completer=completer, style=style, history=history).strip()
        
            if user_input == '':
                if parent:
                    contestList(db[parent])
                else:
                    print(colored_text('\n'.join(list(db.keys())), 'magneta'))
           # handle clear command
            elif user_input.lower() == 'clear':
                clear_terminal()
            elif user_input.lower() == 'exit':
                sys.exit(0)
            elif user_input == '..':
                parent = None
            elif parent and user_input in db[parent][0]:
                showInfo(getInfo(getAddress(db[parent], user_input)))
            elif not parent and user_input in list(db.keys()):
                parent = user_input
            elif parent and user_input.startswith('cp '):
                if user_input[3:] in db[parent][0]:
                    copyContest(getAddress(db[parent], user_input[3:]))
                else:
                    print(colored_text(f'contest by name {user_input[5:]} not found!', 'red'))
            elif parent and user_input.startswith('code '):
                if user_input[5:] in db[parent][0]:
                    openCode(getAddress(db[parent], user_input[5:]))
                else:
                    print(colored_text(f'contest by name {user_input[5:]} not found!', 'red'))
            else:
                print(colored_text('invalid command or contest not found!', 'red'))

        # Graceful exit on Ctrl+C
        except KeyboardInterrupt:
            print(colored_text('bye bye!','yellow'))
            sys.exit(0)

        # Catch unexpected errors
        except Exception as e:
            raise Exception(f'We have some Error: {e}')