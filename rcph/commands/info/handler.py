from rcph.utils.launcher import currentIsContest
from .info import showInfo
from .edit import editContest
from .status import setMultiStatus, setStatus, problemCheck, queraEdit
from .parent import showParents, addParent, chooseParent
from .db import showDBstatus, add2DB, rm2DB

def run(args):
    if not currentIsContest():
        raise Exception('You are not in a contest directory!')

    if args.subcommand1:
        if args.subcommand1 == 'edit':
            editContest()
        elif args.subcommand1 == 'status':
            if args.subcommand2 == '.':
                setMultiStatus()
            elif args.subcommand2:
                problemCheck(args.subcommand2)
                setStatus(args.subcommand2)
            else:
                raise Exception(f'subcommand2 (problem letter) is required!')
        elif args.subcommand1 == 'quera':
            if args.subcommand2:
                problemCheck(args.subcommand2)
                queraEdit(args.subcommand2)
            else:
                raise Exception(f'subcommand2 (problem letter) is required!')
        elif args.subcommand1 == 'parent':
            if args.subcommand2 == '+':
                addParent()
            elif args.subcommand2 == 'choose':
                chooseParent()
            else:
                showParents()
        elif args.subcommand1 == 'db':
            if args.subcommand2 == 'add':
                add2DB()
            elif args.subcommand2 == 'rm':
                rm2DB()
            else:
                showDBstatus()
    else:
        showInfo()