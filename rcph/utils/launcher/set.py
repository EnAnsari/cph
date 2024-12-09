from rcph.utils.imports import os, json
from rcph.config.constant import *
from rcph.config.data import DATA_ADDRESS

def _jsonSet(jsonfile, address):
    with open(address, 'w') as f:
        json.dump(jsonfile, f, indent=4)

def _writeFile(file, address):
    with open(address, 'w') as f:
        f.write(file)

def setInfo(info, address=None): # local config
    _jsonSet(info, os.path.join(address if address else os.getcwd(), CURRENT.RCPH_FOLDER, CURRENT.CONTEST_INFO_JSON))

def setLastJudge(problem):
    _writeFile(problem, os.path.join(os.getcwd(), CURRENT.RCPH_FOLDER, CURRENT.LASTJUDGE))

def setConnection(connection):
    _jsonSet(connection, os.path.join(DATA_ADDRESS, DATA.DB_FOLDER, DATA.CONNECTION_JSON))

def setParents(parent):
    _jsonSet(parent, os.path.join(DATA_ADDRESS, DATA.DB_FOLDER, DATA.PARENT_FILE))

# def makeProblemScript():
#     pass

def setContestDB(db):
    _jsonSet(db, os.path.join(DATA_ADDRESS, DATA.DB_FOLDER, DATA.CONTEST_DB_NAME))
