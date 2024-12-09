from rcph.utils.launcher import getParents, setParents, getInfo, setInfo
from rcph.utils.tools.color import colored_text
from rcph.config.constant import *

def showParents():
    parents = getParents()

    print(colored_text('current parents:', 'yellow'))
    print(colored_text(', '.join(parents), 'green'))

def addParent():
    new_parent = input(colored_text('Enter a new name parent: ', 'yellow'))
    if not new_parent:
        return # cancel by empty input
    
    parents = getParents()
    if new_parent in parents:
        print(colored_text('This parent was exist before! please try another one!', 'red'))
        return addParent()
    
    parents.append(new_parent)
    setParents(parents)
    print(colored_text(f'{new_parent} added successfully!', 'green'))

def chooseParent():
    info = getInfo()
    parents = getParents()
    print(colored_text('this parent of contest is:', 'blue'), colored_text(info[DICT.PARENT], 'green', 'bold'))
    print(colored_text('Existing parents:', 'yellow'))
    print(colored_text(', '.join(parents), 'green'))
    new_parent = input(colored_text('Enter new parent of this contest: ', 'yellow'))
    if not new_parent in parents:
        raise Exception(f'{new_parent} doesn\'t exist in parents list!')
    info[DICT.PARENT] = new_parent
    setInfo(info)
    print(colored_text('parent of contest updated successfully!', 'green'))