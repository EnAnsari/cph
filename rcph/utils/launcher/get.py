from rcph.utils.imports import os, json, pkg_resources
from rcph.config.constant import *

def getInfo():
    with open(os.path.join(os.getcwd(), RCPH_FOLDER, CONTEST_INFO_JSON), 'r') as file:
        info = json.load(file)
    return info

def getLastJudge():
    last_judge_file = os.path.join(os.getcwd(), RCPH_FOLDER, LASTJUDGE)
    if not os.path.exists(last_judge_file):
        raise Exception('There is not any last judge! please enter someone...')
    with open(last_judge_file, 'r') as file:
        problem = file.read()
    return problem

def getGlobaltConfig():
    with pkg_resources.open_text(CONFIG_FOLDER, GLOBAL_CONFIG) as json_file:
        config = json.load(json_file)
    
    return config

def isDevMode(): # am I using this app developer mode or normal mode?
    config = getGlobaltConfig()
    return config['debug']

def getTemplate():
    with pkg_resources.open_text(TEMPLATE_FOLDER, DATA_TEMPLATE_CPP) as template_file:
        template = template_file.read()
    
    return template

def getQuote():
    with pkg_resources.open_text(DB_FOLDER, QUOTES_FILE) as quotes_file:
        quotes = quotes_file.readlines()
    
    return quotes

def getSign():
    with pkg_resources.open_text(DB_FOLDER, SIGN_FILE) as sign_file:
        sign = sign_file.readlines()
    
    return sign