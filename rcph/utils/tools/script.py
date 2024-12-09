from .sign import makeSign
from ..launcher import getTemplate, getGlobaltConfig
from rcph.config.constant import *

def getProblemScript(contest_path, problem_letter, script=None):
    """
    creating problem script
    Args:
        problem letter
    """
    template = script if script else getTemplate()
    config = getGlobaltConfig()
    sign_flag = config[DICT.SIGN]

    if sign_flag:
        if config[DICT.SIGN_DETAIL][DICT.SIDE] == DICT.TOP:
            script = makeSign(contest_path, problem_letter) + '\n' + template
        else: # bottom
            script = template + '\n' + makeSign(contest_path, problem_letter)
    else:
        script = template
        
    return script