from rcph.utils.imports import os, Completer, Completion
from rcph.utils.tools.color import colored_text

class DirectoryCompleter(Completer):
    def __init__(self, get_cwd, hidden_items, shortcut={}):
        self.get_cwd = get_cwd
        self.hidden_items = hidden_items
        self.shortcut = shortcut

    def get_completions(self, document, complete_event):
        text = document.text
        dir = os.path.join(self.get_cwd(), *text.split('/')[:-1])
        text = text.split('/')[-1]
        try:
            if dir in self.shortcut:
                items = self.shortcut[dir]
            else:
                items = sorted(os.listdir(dir))
            if not self.hidden_items:
                items = [item for item in items if not item.startswith('.')]
        except PermissionError:
            items = []
        
        for item in items:
            if item.lower().startswith(text.lower()):
                if os.path.isdir(os.path.join(self.get_cwd(), item)):
                    yield Completion(item, start_position=-len(text), style='fg:ansiblue bold')
                else:
                    yield Completion(item, start_position=-len(text), style='fg:ansiyellow')


def advancedListDIR(curr, hidden_items, shortcut={}):
    try:
        if curr in shortcut:
            items = shortcut[curr]
        else:
            items = sorted(os.listdir(curr))
        
        if not items:
            print(colored_text("No files or directories in this directory.", 'red'))

        if not hidden_items:
            items = [item for item in items if not item.startswith('.')]

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
            if file.endswith('.h') or file.endswith('.hpp'):
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
        print(colored_text("Permission denied!", 'red'))