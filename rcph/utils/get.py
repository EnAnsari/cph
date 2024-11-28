from rcph.utils import os, json
from rcph.config.constant import *

def getInfo():
    with open(os.path.join(os.getcwd(), RCPH_FOLDER, CONTEST_INFO_JSON), 'r') as file:
        info = json.load(file)
    return info


def setInfo(info):
    with open(os.path.join(os.getcwd(), RCPH_FOLDER, CONTEST_INFO_JSON), 'w') as file:
        json.dump(info, file, indent=4)


def getLastJudge():
    last_judge_file = os.path.join(os.getcwd(), RCPH_FOLDER, LASTJUDGE)
    if not os.path.exists(last_judge_file):
        raise Exception('There is not any last judge! please enter someone...')
    with open(last_judge_file, 'r') as file:
        problem = file.read()
    return problem


def setLastJudge(problem):
    last_judge_file = os.path.join(os.getcwd(), RCPH_FOLDER, LASTJUDGE)
    with open(last_judge_file, 'w') as file:
        file.write(problem)


def getGlobaltConfig():
    here = os.path.dirname(os.path.abspath(__file__))
    config_path = os.path.join(here, *['..'] * 2, COMPONENTS, CONFIG_FOLDER, GLOBAL_CONFIG)
    with open(config_path, 'r') as json_file:
        config = json.load(json_file)
    
    return config


def getTemplate():
    here = os.path.dirname(__file__)
    template = os.path.join(here, *['..'] * 2, COMPONENTS, TEMPLATE_FOLDER, COMPONENT_TEMPLATE_CPP)
    return template