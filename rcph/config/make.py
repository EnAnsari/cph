from rcph.utils import json, os
from rcph.config.constant import *

def run(folder_path, contest_path, contest):
    here = os.path.dirname(os.path.abspath(__file__))
    config_path = os.path.join(here, *['..'] * 2, COMPONENTS, CONFIG_FOLDER, GLOBAL_CONFIG)
    with open(config_path, 'r') as json_file:
        config = json.load(json_file)

    data = {
        'name': contest['name'],
        'parent': config["default parent"],
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
