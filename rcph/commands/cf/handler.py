from .utils import checkCFlink, scrape
from rcph.utils.launcher import currentIsContest

def run():
    if not currentIsContest():
        raise Exception('You are not in a contest directory!')

    checkCFlink()
    scrape()
