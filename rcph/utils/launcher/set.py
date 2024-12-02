from rcph.utils.imports import os, json, pkg_resources
from rcph.config.constant import *

def setInfo(info):
    with open(os.path.join(os.getcwd(), RCPH_FOLDER, CONTEST_INFO_JSON), 'w') as file:
        json.dump(info, file, indent=4)


def setLastJudge(problem):
    last_judge_file = os.path.join(os.getcwd(), RCPH_FOLDER, LASTJUDGE)
    with open(last_judge_file, 'w') as file:
        file.write(problem)


def updateDBcontest(contest_address):
    with pkg_resources.open_text(DB_FOLDER, QUOTES_FILE) as quotes_file:
        quotes = quotes_file.readlines()
    contestDB_path = os.path.join(here, *['..'] * 3, COMPONENTS, DB_FOLDER, CONTEST_DB_NAME)

    if os.path.exists(contestDB_path):
        with open(contestDB_path, 'r') as contestDB_file:
            contestDB = json.load(contestDB_file)
    else:
        contestDB = []

    contestDB.append(folder_path)
    with open(contestDB_path, 'w') as contestDB_file:
        json.dump(contestDB, contestDB_file, indent=4)