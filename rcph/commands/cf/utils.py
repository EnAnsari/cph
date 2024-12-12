from rcph.utils.imports import os, re, Service, Options, BeautifulSoup, webdriver
from rcph.utils.launcher import getInfo, setInfo, getConnection
from rcph.utils.tools.script import getProblemScript
from rcph.utils.tools.color import colored_text
from rcph.commands.resign.utils import multiResign
from rcph.config.constant import *



def checkCFlink():
    info = getInfo()
    url = info[DICT.LINK]
    pattern = r"^https://codeforces\.com/contest/\d+/?$"
    if not re.match(pattern, url):
        raise Exception('link invalid and it is not a codeforces link!')

def getSoup():
    info = getInfo()
    if info[DICT.LINK].endswith('/'):
        url = info[DICT.LINK] + 'problems'
    else:
        url = info[DICT.LINK] + '/problems'

    chrome_options = Options()
    # chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")

    connection = getConnection()
    if not DATA.CHROMEDRIVER in connection or not os.path.exists(connection[DATA.CHROMEDRIVER]):
        raise Exception('chrome driver not exist! please connect somewhere first!')
    
    try:
        chromedrive_path = connection[DATA.CHROMEDRIVER]
        service = Service(chromedrive_path)
        driver = webdriver.Chrome(service=service, options=chrome_options)
    except Exception as e:
        raise Exception(f'chrome driver path in connection.json is incorrect!')

    try:
        # Open the page
        driver.get(url)

        # Wait for the page to load fully (if needed)
        driver.implicitly_wait(5000)

        # Get the page source
        page_source = driver.page_source

        # Parse with Beautiful Soup
        soup = BeautifulSoup(page_source, 'html.parser')

    except Exception as e:
        raise Exception('contest not find!')

    finally:
        # Quit the driver
        driver.quit()
    
    return soup

def createProblem(info, problem):
    info[DICT.PROBLEMS].append({
        DICT.LETTER: problem['letter'],
        DICT.NAME: problem['name'],
        DICT.STATUS: DICT.NULL
    })
    os.mkdir(os.path.join(os.getcwd(), CURRENT.RCPH_FOLDER, CURRENT.TESTCASE_FOLDER, problem['letter'])) # create problem tc folder
    with open(os.path.join(os.getcwd(), problem['letter'] + '.cpp'), 'w') as f:
        f.write(getProblemScript(os.getcwd(), problem['letter'])) # create script

    return info

def addProblem(info, problem):
    find_flag = False
    for p in info[DICT.PROBLEMS]:
        if p[DICT.LETTER] == problem['letter']:
            p[DICT.NAME] = problem['name']
            find_flag = True
    
    if not find_flag:
        info = createProblem(info, problem)

    i = 1
    tc_folder = os.path.join(os.getcwd(), CURRENT.RCPH_FOLDER, CURRENT.TESTCASE_FOLDER, problem['letter'])
    for fin_content, fout_content in zip(problem['input'], problem['output']):
        with open(os.path.join(tc_folder, str(i) + '.in'), 'w') as fin, open(os.path.join(tc_folder, str(i) + '.ans'), 'w') as fout:
            fin.write(fin_content)
            fout.write(fout_content)
        i += 1

    return info

def applyChanges(info, problems):
    for problem in problems:
        info = addProblem(info, problem)

    return info


def scrape():
    soup = getSoup()
    info = getInfo()
    try:
        info[DICT.DETAIL] = soup.find('div', class_='caption').get_text(strip=True)
    except Exception as e:
        raise Exception('contest loading faild!')

    problems_for_save = []
    for problem in soup.find_all('div', class_='ttypography'):
        problem_name = problem.find('div', class_='title').get_text(strip=True)
        match = re.match(r'([A-Za-z0-9]+)\.\s*(.*)', problem_name)
        problem_dict = {
            'letter': match.group(1).lower(),
            'name': match.group(2),
            'input': [],
            'output': []
        }

        for inp in problem.find_all('div', class_='input'):
            if inp.find('pre').find_all('div'):
                total_input = []
                for inp_line in inp.find('pre').find_all('div'):
                    total_input.append(inp_line.get_text(strip=True))
                problem_dict['input'].append('\n'.join(total_input))
            else:
                problem_dict['input'].append(inp.find('pre').get_text(strip=True))

        for outp in problem.find_all('div', class_='output'):
            problem_dict['output'].append(outp.find('pre').get_text(strip=True))

        problems_for_save.append(problem_dict)

    info = applyChanges(info, problems_for_save)
    setInfo(info)
    multiResign(silent=True)
    print(colored_text(f'contest loaded successfully ({len(problems_for_save)} problems updated)!', 'green'))