from rcph.utils.imports import os, json
from rcph.config.constant import *
from rcph.config.data import DATA_ADDRESS

def _getJson(address):
    with open(address, 'r') as f:
        result = json.load(f)
    return result

def _readFile(address):
    with open(address, 'r') as f:
        result = f.read()
    return result

def _readLinesFile(address):
    with open(address, 'r') as f:
        result = f.readlines()
    return result

def currentIsContest(address=None):
    here = address if address else os.getcwd()
    local_info = os.path.join(here, CURRENT.RCPH_FOLDER, CURRENT.CONTEST_INFO_JSON)
    return os.path.exists(local_info)

def getInfo(address=None): # local config
    return _getJson(os.path.join(address if address else os.getcwd(), CURRENT.RCPH_FOLDER, CURRENT.CONTEST_INFO_JSON))

def getLastJudge():
    last_judge_file = os.path.join(os.getcwd(), CURRENT.RCPH_FOLDER, CURRENT.LASTJUDGE)
    if not os.path.exists(last_judge_file):
        raise Exception('There is not any last judge! please enter someone...')
    return _readFile(last_judge_file)

def getGlobaltConfig():
    return _getJson(os.path.join(DATA_ADDRESS, DATA.CONFIG_FOLDER, DATA.GLOBAL_CONFIG))

def isDevMode(): # am I using this app developer mode or normal mode?
    config = getGlobaltConfig()
    return config[DICT.DEBUG]

def getTemplate():
    return _readFile(os.path.join(DATA_ADDRESS, DATA.TEMPLATE_FOLDER, DATA.TEMPLATE_CPP))
    
def getQuote():
    return _readLinesFile(os.path.join(DATA_ADDRESS, DATA.DB_FOLDER, DATA.QUOTES_FILE))

def getSign():
    return _readLinesFile(os.path.join(DATA_ADDRESS, DATA.DB_FOLDER, DATA.SIGN_FILE))

def testCounter(problem):
    result = 1
    problemFolder = os.path.join(os.getcwd(), CURRENT.RCPH_FOLDER, CURRENT.TESTCASE_FOLDER, problem)
    while os.path.exists(os.path.join(problemFolder, str(result) + '.in')) and os.path.exists(os.path.join(problemFolder, str(result) + '.ans')):
        result += 1
    return result - 1


def getConnection():
    connection_file_path = os.path.join(DATA_ADDRESS, DATA.DB_FOLDER, DATA.CONNECTION_JSON)
    try:
        if not os.path.exists(connection_file_path):
            # raise Exception('There is not any connection! please make someone...')
            return {}
        with open(connection_file_path, 'r') as connection_file:
            connection = json.load(connection_file)
    except:
        connection = {}
    return connection


def getAssetDirectory():
    connection = getConnection()
    return connection[DATA.ASSET_FOLDER]


def getParents():
    parent_path= os.path.join(DATA_ADDRESS, DATA.DB_FOLDER, DATA.PARENT_FILE)
    if not os.path.exists(parent_path):
        raise Exception('There is not any parents file in data/db!')
    return _getJson(parent_path)

def getContestDB():
    contestDB_path = os.path.join(DATA_ADDRESS, DATA.DB_FOLDER, DATA.CONTEST_DB_NAME)
    if os.path.exists(contestDB_path):
        contestDB = _getJson(contestDB_path)
    else:
        contestDB = []
    return contestDB

def checkExistenceProblem(problem_letter):
    info = getInfo()
    for p in info[DICT.PROBLEMS]:
        if p[DICT.LETTER] == problem_letter:
            return True
    return False

def getAssetShortcuts():
    connection = getConnection()
    if not connection:
        raise Exception('connection file is empty!')
    shorcut_path = os.path.join(connection[DATA.ASSET_FOLDER], '.shortcut.json')
    if not os.path.exists(shorcut_path):
        return {}
    shorcut = _getJson(shorcut_path)
    return {os.path.join(connection[DATA.ASSET_FOLDER], *key.split('/')[1:]) : value for key, value in shorcut.items()}