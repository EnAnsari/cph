from rcph.utils.imports import os
from rcph.config.constant import *
from rcph.utils.launcher import getGlobaltConfig

# making .rcph/info.json
def makeLocalConfig(contest_path, contest_link, parent, problems):
    config = getGlobaltConfig()

    data = {
        DICT.NAME: os.path.basename(contest_path),
        DICT.PARENT: parent,
        DICT.PATH: contest_path,
        DICT.LINK: contest_link,
        DICT.DETAIL: '',
        DICT.REPO: '',
        DICT.PROBLEMS: [],
    }

    for problem_letter in problems:
        problem = {
            DICT.LETTER: problem_letter,
            DICT.NAME: '',
            DICT.STATUS: DICT.NULL,
        }
        
        data[DICT.PROBLEMS].append(problem)
    return data
    
