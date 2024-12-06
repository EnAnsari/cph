from .utils import *

def run(args):
    operation = None
    if args.plus:
        if args.plus == '+':
            operation = 'add'
        elif args.plus == 'choose':
            operation = 'choose'

    if operation == 'add':
        addParent()
    elif operation == 'choose':
        pass # you should complete this!
    else:
        showParents()