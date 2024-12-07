from rcph.utils.imports import os, datetime, json
from .quote import make_a_quote
from rcph.config.constant import *
from ..launcher import getSign, getQuote, getGlobaltConfig

def makeSign(folder_path, problem_letter):

    quotes = getQuote()
    local_sign = getSign()
    config = getGlobaltConfig()

    with open(os.path.join(folder_path, RCPH_FOLDER, CONTEST_INFO_JSON), 'r') as file:
        contest = json.load(file)

    sign_content = '/*\n'

    if config[DICT.SIGN_DETAIL][DICT.CONTEST_INFO]:
        sign_content += f'\tcontest name: {contest["name"]}\n' if contest['name'] else ''
        sign_content += f'\tcontest link: {contest["link"]}\n' if contest['link'] else ''
        sign_content += f'\tmy code repository: {contest["repo"]}\n' if contest['repo'] else ''

        problem_name = ''
        for problem in contest['problems']:
            if problem['letter'] == problem_letter:
                problem_name = problem['name']
                break

        sign_content += f'\tproblem name: {problem_name}\n' if problem_name else ''
        sign_content += f'\tproblem letter: {problem_letter.upper()}\n'
        sign_content += f'\tTime: {datetime.datetime.now().strftime("%Y-%m-%d %H:%M")}\n\n' # Time

    if config[DICT.SIGN_DETAIL][DICT.PERSONAL_SIGN]:
        for line in local_sign:
            sign_content += f'\t{line.strip()}\n'

    if config[DICT.SIGN_DETAIL][DICT.QUOTE]:
        sign_content += f'\n{make_a_quote(quotes)}\n\n'
    
    if config[DICT.SIGN_DETAIL][DICT.ABOUT]:
        sign_content += f'\tthis code created by rcph (https://github.com/EnAnsari/cph)\n'
    
    sign_content += '*/'

    return sign_content