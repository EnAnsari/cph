MAXSIGNLINE = 20 # Related to quote

# current contest
class CURRENT:
    CONTEST_INFO_JSON = 'info.json'
    TESTCASE_FOLDER = 'tc'
    RCPH_FOLDER = '.rcph'
    TEMPLATE_CPP = 'template.cpp'
    LASTJUDGE = 'lastjudge.txt'

    # input/output mode file names
    INPUT_FILE = 'input.txt'
    OUTPUT_FILE = 'output.txt'

# global folder (data)
class DATA:
    # folders
    TEMPLATE_FOLDER = 'template'
    CONFIG_FOLDER = 'config'
    DB_FOLDER = 'db'

    TEMPLATE_CPP = 'template.cpp' # in template folder
    GLOBAL_CONFIG = 'contest.json' # in config folder
    CONTEST_DB_NAME = 'contests.json' # in db folder
    QUOTES_FILE = 'quotes.txt'
    SIGN_FILE = 'sign.txt'
    CONNECTION_JSON = 'connection.json'
    ASSET_FOLDER = 'asset' # a folder for saving assets
    SAVED = 'saved' # in asset folder for saving my assets
    PARENT_FILE = 'parents.json'

# dictionary keys
class DICT:
    DEFAULT_PARENT = 'default parent'
    SIGN = 'sign'
    SIGN_DETAIL = 'sgin detail'
    SIDE = 'side'
    CONTEST_INFO = 'contest info'
    PERSONAL_SIGN = 'personal sign'
    QUOTE = 'quote'
    ABOUT = 'about'
    DEBUG = 'debug'
    
    # contest info file
    NAME = 'name'
    LINK = 'link'
    DETAIL = 'detail'
    REPO = 'repo'
    LETTER = 'letter'
    PARENT = 'parent'
    PATH = 'path'
    PROBLEMS = 'problems'
    STATUS = 'status'
    NULL = 'null'
    TOP = 'top'

class COMMANDS:
    CLEAR = ['clear', 'delete'] # for test cases
    EMPTY = '--'
    TEST = 'test'
    INPUT = 'input'
    DOMJUDGE = 'domjudge'
    LS_BY_ENTER = 'ls by enter'
    HIDDEN_ITEMS = 'hidden items'

# commands/info/status.py
class PROBLEM_STATUS:
    class COMMAND:
        WRONG_ANSWER = ['wrong answer', 'wa',  'wrong']
        ACCEPT = ['accept', 'correct', 'acc']
        RAW = ['raw']
        NULL = ['null', 'none']
    class STATUS:
        WRONG_ANSWER = 'Wrong Answer'
        ACCEPT = 'Accept'
        RAW = 'raw'
        NULL = 'null'