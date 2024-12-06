from rcph.utils.imports import os
from rcph.utils.launcher import getParents, setParents
from rcph.utils.tools.color import colored_text

def showParents():
    parents = getParents()

    print(colored_text('current parents:', 'yellow'))
    print(colored_text(', '.join(parents), 'green'))

def addParent():
    new_parent = input(colored_text('Enter a new name parent: ', 'yellow'))
    if not new_parent:
        return
    
    parents = getParents()
    if new_parent in parents:
        print(colored_text('This parent was exist before! please try another one!', 'red'))
        return addParent()
    
    parents.append(new_parent)
    setParents(parents)
    print(colored_text(f'{new_parent} added successfully!', 'green'))