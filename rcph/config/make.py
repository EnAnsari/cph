from rcph.utils.imports import json, os
from rcph.config.constant import *
from rcph.utils.launcher import getGlobaltConfig

def makeLocalConfig(folder_path, contest_path, contest, parent):
    config = getGlobaltConfig()

    data = {
        'name': contest['name'],
        'parent': config["default parent"] if parent == '' else parent,
        'path': contest_path,
        'link': contest['link'],
        'detail': contest['detail'],
        'repo': contest['repo'],
        'problems': [],
    }

    for problem_letter in contest['problems']:
        problem = {
            'letter': problem_letter,
            'name': '',
            'status': 'null',
            'test case': 0
        }
        
        data['problems'].append(problem)

    with open(os.path.join(folder_path, CONTEST_INFO_JSON), 'w') as json_file:
        json.dump(data, json_file, indent=4)
