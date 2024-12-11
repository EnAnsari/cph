from rcph.utils.imports import os
from rcph.utils.launcher import getContestDB, setContestDB, getInfo
from rcph.utils.tools.color import colored_text
from rcph.config.constant import *

def getContestPath():
    return getInfo()[DICT.PATH]

def contestExsitInDB():
    db = getContestDB()
    if getContestPath() in db:
        return True
    else:
        return False

def showDBstatus():
    if contestExsitInDB():
        print(colored_text('contest directory exist in contest DB!', 'green'))
    else:
        print(colored_text('contest directory doesn\'t exist in contest DB!', 'red'))

def add2DB():
    contest_path = getContestPath()
    db = getContestDB()
    if contest_path in db:
        raise Exception('contest exist in DB before!')
    db.append(contest_path)
    setContestDB(db)
    result_message = 'contest ' + colored_text('added', 'green', 'bold') + ' to DB ' + colored_text('successfully!', 'green')
    print(result_message)

def rm2DB():
    contest_path = getContestPath()
    db = getContestDB()
    if not contest_path in db:
        raise Exception('contest doesn\'t exist in DB before!')
    db.remove(contest_path)
    setContestDB(db)
    result_message = 'contest ' + colored_text('removed', 'red', 'bold') + ' from DB ' + colored_text('successfully!', 'green')
    print(result_message)