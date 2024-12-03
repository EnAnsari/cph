from rcph.utils.imports import json, os
from rcph.config.constant import *
from rcph.utils.launcher import getGlobaltConfig

def makeLocalConfig(folder_path, contest_path, contest, parent):
    config = getGlobaltConfig()

    data = {
        DICT.NAME: contest[DICT.NAME],
        DICT.PARENT: config[DICT.DEFAULT_PARENT] if parent == '' else parent,
        DICT.PATH: contest_path,
        DICT.LINK: contest[DICT.LINK],
        DICT.DETAIL: contest[DICT.DETAIL],
        DICT.REPO: contest[DICT.REPO],
        DICT.PROBLEMS: [],
    }

    for problem_letter in contest[DICT.PROBLEMS]:
        problem = {
            DICT.LETTER: problem_letter,
            DICT.NAME: '',
            DICT.STATUS: DICT.NULL,
        }
        
        data[DICT.PROBLEMS].append(problem)

    with open(os.path.join(folder_path, CONTEST_INFO_JSON), 'w') as json_file:
        json.dump(data, json_file, indent=4)
