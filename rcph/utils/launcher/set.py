from rcph.utils.imports import os, json
from rcph.config.constant import *
from rcph.config.data import DATA_ADDRESS

def setInfo(info):
    with open(os.path.join(os.getcwd(), RCPH_FOLDER, CONTEST_INFO_JSON), 'w') as file:
        json.dump(info, file, indent=4)


def setLastJudge(problem):
    last_judge_file = os.path.join(os.getcwd(), RCPH_FOLDER, LASTJUDGE)
    with open(last_judge_file, 'w') as file:
        file.write(problem)


def updateDBcontest(contest_address):
    contestDB_path = os.path.join(DATA_ADDRESS, DB_FOLDER, CONTEST_DB_NAME)
    if os.path.exists(contestDB_path):
        with open(contestDB_path, 'r') as contestDB_file:
            contestDB = json.load(contestDB_file)
    else:
        contestDB = []

    contestDB.append(contest_address)
    with open(contestDB_path, 'w') as contestDB_file:
        json.dump(contestDB, contestDB_file, indent=4)


def setConnection(connection):
    with open(os.path.join(DATA_ADDRESS, DB_FOLDER, CONNECTION_JSON), 'w') as connection_file:
        json.dump(connection, connection_file, indent=4)

def setParents(parent):
    parent_path= os.path.join(DATA_ADDRESS, DB_FOLDER, PARENT_FILE)
    with open(parent_path, 'w') as parent_file:
        json.dump(parent, parent_file, indent=4)