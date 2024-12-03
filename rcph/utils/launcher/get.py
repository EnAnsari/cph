from rcph.utils.imports import os, json
from rcph.config.constant import *
from rcph.config.data import DATA_ADDRESS

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
    with open(os.path.join(DATA_ADDRESS, CONFIG_FOLDER, GLOBAL_CONFIG), 'r') as config_file:
        config = json.load(config_file)
    
    return config

def isDevMode(): # am I using this app developer mode or normal mode?
    config = getGlobaltConfig()
    return config[DICT.DEBUG]

def getTemplate():
    with open(os.path.join(DATA_ADDRESS, TEMPLATE_FOLDER, DATA_TEMPLATE_CPP), 'r') as template_file:
        template = template_file.read()
    
    return template

def getQuote():
    with open(os.path.join(DATA_ADDRESS, DB_FOLDER, QUOTES_FILE), 'r') as quotes_file:
        quotes = quotes_file.readlines()
    
    return quotes

def getSign():
    with open(os.path.join(DATA_ADDRESS, DB_FOLDER, SIGN_FILE), 'r') as sign_file:
        sign = sign_file.readlines()
    
    return sign