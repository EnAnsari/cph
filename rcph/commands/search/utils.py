from rcph.utils.imports import os, tqdm, shutil
from rcph.utils.launcher import getInfo, getContestDB, getConnection
from rcph.utils.tools.color import colored_text
from rcph.config.constant import *
from rcph.commands.globall.utils import copyContest

def contestName():
    name = input(colored_text('Enter Contest Name for Search (. for current contest name): ', 'yellow')).strip()
    if name == '':
        return # canceling
    if name == '.':
        name = getInfo()[DICT.NAME]
    db = getContestDB()
    counter = 0
    for contest in tqdm.tqdm(db, desc='searching', leave=False):
        if os.getcwd().replace('\\', '/') == contest:
            continue
        if not os.path.exists(contest):
            print(colored_text(f'contest by path {contest} not exist!', 'red'))
            continue
        contest_info = getInfo(contest)
        if name.lower() in contest_info[DICT.NAME].lower():
            print(colored_text(f'> contest name found: {contest_info[DICT.NAME]} by {len(contest_info[DICT.PROBLEMS])} problem!', 'green', 'bold'))
            counter += 1
            copyContest(contest, os.path.join('search', 'contest_name'))
    print(colored_text(f'search completed! {counter} case found!', 'magneta'))


def problemName():
    name = input(colored_text('Enter problem Name for Search (. for every problems): ', 'yellow')).strip()
    if name == '.':
        name = [problem[DICT.NAME] for problem in getInfo()[DICT.PROBLEMS] if problem[DICT.NAME]]
    elif name == '':
        return # canceling
    else:
        name = [name]

    db = getContestDB()
    counter = 0
    for contest in tqdm.tqdm(db, desc='searching', leave=False):
        if os.getcwd().replace('\\', '/') == contest:
            continue
        if not os.path.exists(contest):
            print(colored_text(f'contest by path {contest} not exist!', 'red'))
            continue
        contest_info = getInfo(contest)
        contest_problems = [problem for problem in contest_info[DICT.PROBLEMS] if problem[DICT.NAME]]
        found_flag = False
        for problem_name in name:
            for contest_problem in contest_problems:
                if problem_name.lower() in contest_problem[DICT.NAME].lower():
                    print(colored_text(f'problem found: {problem_name} -> {contest_problem[DICT.NAME]} (problem {contest_problem[DICT.LETTER]} in {contest_info[DICT.NAME]}, status: {contest_problem[DICT.STATUS]})', 'green', 'bold'))
                    found_flag = True
        if found_flag:
            copyContest(contest, os.path.join('search', 'problem_name'))
    print(colored_text(f'search completed! {counter} case found!', 'magneta'))

def getProblemLetters():
    user_input = input(colored_text('Enter problem letters for search (. for everyone): ', 'yellow')).strip()
    if user_input == '.':
        problem2search = [problem[DICT.LETTER] for problem in getInfo()[DICT.PROBLEMS]]
    elif user_input == '':
        return # canceling
    else:
        problem2search = []
        for problem in user_input.split():
            if os.path.exists(os.path.join(os.getcwd(), CURRENT.RCPH_FOLDER, CURRENT.TESTCASE_FOLDER, problem)):
                problem2search.append(problem)
            else:
                print(colored_text(f'problem {problem} not found!', 'red'))
    return problem2search

def tcSaved():
    problem2search = getProblemLetters()
    db = getContestDB()
    counter = 0
    for contest in tqdm.tqdm(db, desc='searching', leave=False): # iterate in contests in db (1)
        if os.getcwd().replace('\\', '/') == contest:
            continue
        if not os.path.exists(contest):
            print(colored_text(f'contest by path {contest} not exist!', 'red'))
            continue
        found_flag = False
        
        target_tc_folder = os.path.join(contest, CURRENT.RCPH_FOLDER, CURRENT.TESTCASE_FOLDER)
        for problem_letter in sorted(os.listdir(target_tc_folder)): # iterate in problems in target contest (2) 
            problem_tc_folder = os.path.join(target_tc_folder, problem_letter)
            
            # current test case folder
            for current in problem2search: # iterate in source problems (3)
                current_tc_folder = os.path.join(os.getcwd(), CURRENT.RCPH_FOLDER, CURRENT.TESTCASE_FOLDER, current)

                i = 1 # iterate in target problem test cases (4)
                while os.path.exists(os.path.join(problem_tc_folder, str(i) + '.in')) and os.path.exists(os.path.join(problem_tc_folder, str(i) + '.ans')):
                    j = 1 # iterate in source problem test cases (5)
                    while os.path.exists(os.path.join(current_tc_folder, str(j) + '.in')) and os.path.exists(os.path.join(current_tc_folder, str(j) + '.ans')):
                        fin_src = os.path.join(current_tc_folder, str(j) + '.in')
                        fout_src = os.path.join(current_tc_folder, str(j) + '.ans')
                        fin_des = os.path.join(problem_tc_folder, str(i) + '.in')
                        fout_des = os.path.join(problem_tc_folder, str(i) + '.ans')
                        with open(fin_src, 'r') as fis, open(fout_src, 'r') as fos, open(fin_des, 'r') as fid, open(fout_des, 'r') as fod:
                            if fis.read().strip() == fid.read().strip() and fos.read().strip() == fod.read().strip():
                                message = colored_text('test case found: ', 'green')
                                message += colored_text(f'test case number {j} in problem {current.upper()} founded in ', 'yellow')
                                message += colored_text(f'test case number {i} in problem {problem_letter.upper()} in {getInfo(contest)[DICT.NAME]}, status: {list(problem for problem in getInfo(contest)[DICT.PROBLEMS] if problem_letter == problem[DICT.LETTER])[0][DICT.STATUS]}', 'cyan')
                                print(message)
                                found_flag = True
                                counter += 1
                        j += 1
                    i += 1

        if found_flag:
            copyContest(contest, os.path.join('search', 'tc_saved'))
    print(colored_text(f'search completed! {counter} case found!', 'magneta'))

def tcbank():
    connection = getConnection()
    if not connection or not DATA.TCBANK in connection:
        raise Exception('tcbank not found! please connect somewhere first... (by rcph search connect)')
    tcbank_path = connection[DATA.TCBANK]
    problem2search = getProblemLetters()
    counter = 0
    for contest in tqdm.tqdm(sorted(os.listdir(tcbank_path)), desc='searching', leave=False): # iterate in contest data (1)
        for target_problem in sorted(os.listdir(os.path.join(tcbank_path, contest))): # iterate in problems of a contest (2)
            target_tc_folder = os.path.join(tcbank_path, contest, target_problem)
            found_flag = False
            for source_problem in problem2search: # iterate in current contest problems (3)
                i = 1
                source_tc_folder = os.path.join(os.getcwd(), CURRENT.RCPH_FOLDER, CURRENT.TESTCASE_FOLDER, source_problem)
                while os.path.exists(os.path.join(source_tc_folder, str(i) + '.in')) and os.path.exists(os.path.join(source_tc_folder, str(i) + '.ans')):
                    j = 1
                    while os.path.exists(os.path.join(target_tc_folder, str(j) + '.in')) and os.path.exists(os.path.join(target_tc_folder, str(j) + '.ans')):
                        fin_src = os.path.join(source_tc_folder, str(i) + '.in')
                        fout_src = os.path.join(source_tc_folder, str(i) + '.ans')
                        fin_des = os.path.join(target_tc_folder, str(j) + '.in')
                        fout_des = os.path.join(target_tc_folder, str(j) + '.ans')
                        with open(fin_src, 'r') as fis, open(fout_src, 'r') as fos, open(fin_des, 'r') as fid, open(fout_des, 'r') as fod:
                            if fis.read().strip() == fid.read().strip() and fos.read().strip() == fod.read().strip():
                                message = colored_text('test case found: ', 'green')
                                message += colored_text(f'test case number {i} in problem {source_problem.upper()} founded in ', 'yellow')
                                message += colored_text(f'test case number {j} in problem {target_problem.upper()} in {os.path.basename(contest)}', 'cyan')
                                print(message)
                                found_flag = True
                                counter += 1
                        j += 1
                    i += 1
            if found_flag:
                if os.path.exists(os.path.join(os.getcwd(), 'search', 'tcbank', contest, target_problem)):
                    print(colored_text(f'{os.path.join(contest, target_problem)} founded before!', 'red'))
                else:
                    shutil.copytree(target_tc_folder, os.path.join(os.getcwd(), 'search', 'tcbank', contest, target_problem))
    print(colored_text(f'search completed! {counter} case found!', 'magneta'))


def readInput():
    choices = ['contest name', 'problem name', 'test case of db contest', 'test case bank']
    for i in range(1, len(choices) + 1):
        print(colored_text(f'[{i}]', 'yellow'), colored_text(choices[i - 1], 'green'))
    ch = input(colored_text('search by: ', 'black'))
    
    # error handling
    if not ch.isdigit():
        raise Exception('invalid input!')
    ch = int(ch)
    if ch < 1 or ch > len(choices):
        raise Exception('invalid choice!')
    
    if ch == 1:
        contestName()
    elif ch == 2:
        problemName()
    elif ch == 3:
        tcSaved()
    else:
        tcbank()