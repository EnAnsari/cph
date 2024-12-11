from rcph.utils.imports import datetime
from .quote import make_a_quote
from rcph.config.constant import *
from ..launcher import getSign, getQuote, getGlobaltConfig, getInfo

def makeSign(contest_path, problem_letter):

    quotes = getQuote()
    local_sign = getSign()
    config = getGlobaltConfig()
    contest = getInfo(contest_path)
    local_time = datetime.datetime.now(datetime.timezone.utc).astimezone()
    utc_offset = local_time.utcoffset()
    utc_offset_hours = int(utc_offset.total_seconds() // 3600)
    utc_offset_minutes = int((utc_offset.total_seconds() % 3600) // 60)
    formatted_offset = f"{utc_offset_hours:+}:{utc_offset_minutes:02}"

    sign_content = '/*\n'

    if config[DICT.SIGN_DETAIL][DICT.CONTEST_INFO]:
        sign_content += f'\tcontest name: {contest[DICT.NAME]}\n' if contest[DICT.NAME] else ''
        sign_content += f'\tcontest link: {contest[DICT.LINK]}\n' if contest[DICT.LINK] else ''
        sign_content += f'\tcontest detail: {contest[DICT.DETAIL]}\n' if contest[DICT.DETAIL] else ''
        sign_content += f'\tmy code repository: {contest[DICT.REPO]}\n' if contest[DICT.REPO] else ''

        problem_name = ''
        for problem in contest[DICT.PROBLEMS]:
            if problem[DICT.LETTER] == problem_letter:
                problem_name = problem[DICT.NAME]
                break

        sign_content += f'\tproblem name: {problem_name}\n' if problem_name else ''
        sign_content += f'\tproblem letter: {problem_letter.upper()}\n'
        sign_content += f'\tTime: {local_time.strftime("%Y-%m-%d %H:%M")} UTC: {formatted_offset}\n\n' # Time

    if config[DICT.SIGN_DETAIL][DICT.PERSONAL_SIGN]:
        for line in local_sign:
            sign_content += f'\t{line.strip()}\n'

    if config[DICT.SIGN_DETAIL][DICT.QUOTE]:
        sign_content += f'\n{make_a_quote(quotes)}\n\n'
    
    if config[DICT.SIGN_DETAIL][DICT.ABOUT]:
        sign_content += f'\tthis code created by rcph (https://github.com/EnAnsari/cph)\n'
    
    sign_content += '*/'

    return sign_content