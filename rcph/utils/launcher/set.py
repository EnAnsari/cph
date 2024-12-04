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

def setAssetConnection(address):
    asset = {
        'asset': address
    }
    with open(os.path.join(DATA_ADDRESS, DB_FOLDER, ASSET_JSON), 'w') as asset_bank:
        json.dump(asset, asset_bank, indent=4)

def getAssetDirectory():
    asset_file_path = os.path.join(DATA_ADDRESS, DB_FOLDER, ASSET_JSON)
    if not os.path.exists(asset_file_path):
        return ''
    with open(asset_file_path, 'r') as asset_file:
        asset = json.load(asset_file)
    return asset['asset']