from rcph.utils.imports import os
from rcph.utils.launcher import setAssetConnection
from rcph.utils.tools.color import colored_text

def makeConnection():
    setAssetConnection(os.getcwd())