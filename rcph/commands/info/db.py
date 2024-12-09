from rcph.utils.imports import os
from rcph.utils.launcher import getContestDB, setContestDB
from rcph.utils.tools.color import colored_text
from rcph.config.constant import *

def contestExsitInDB():
    db = getContestDB()
    if os.getcwd() in db:
        return True
    else:
        return False

def showDBstatus():
    if contestExsitInDB():
        print(colored_text('contest directory exist in contest DB!', 'green'))
    else:
        print(colored_text('contest directory doesn\'t exist in contest DB!', 'red'))

def add2DB():
    db = getContestDB()
    if os.getcwd() in db:
        raise Exception('contest exist in DB before!')
    db.append(os.getcwd())
    setContestDB(db)
    result_message = 'contest ' + colored_text('added', 'green', 'bold') + ' to DB ' + colored_text('successfully!', 'green')
    print(result_message)

def rm2DB():
    db = getContestDB()
    if not os.getcwd() in db:
        raise Exception('contest doesn\'t exist in DB before!')
    db.remove(os.getcwd())
    setContestDB(db)
    result_message = 'contest ' + colored_text('removed', 'red', 'bold') + ' from DB ' + colored_text('successfully!', 'green')
    print(result_message)