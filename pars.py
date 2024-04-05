import os
import argparse
import json
import random
import datetime
import subprocess
import timeit
import resource
import zipfile
import importlib.util

""" Infographics
    Hey everyone, I'm Rehmat! I'm excited to jump in and help out the programmer community however I can.
    You can read a useful article about this program in the following link:
    https://github.com/EnAnsari/cp-parser

    Email: Rahmat2022a@gmail.com
    More about me: https://enansari.github.io
"""
# ================================================================ const variables

MAXSIGNLINE = 20
SIGNLINE = 10
ENDTEST = 'ENDTEST'
CANCELTEST = 'CANCELTEST'
CANCELALL = 'CANCELALL'
EMPTY = 'EMPTY'
FILEDIR = os.path.dirname(__file__)
PARSERDIR = os.path.join(os.getcwd(), '.parser')
EMAIL = 'Rahmat2022a@gmail.com'
WEBSITE = 'https://enansari.github.io'
MYNAME = 'Rahmat'


ADDTODB = 1
DEBUG = 1
# if DEBUG:
#     print(colored_text('info file created successfully!', 'light green'))

# ================================================================ public functions

def colored_text(text, color,  *features, reset = True):

    colors = {
        "black": "30",
        "red": "31",
        "green": "32",
        "yellow": "33",
        "blue": "34",
        "magneta": "35",
        "cyan": "36",
        "gray": "37",

        "reset": "0",
        "bold": "1",
        "faint": "2",
        "italic": "3",
        "underline": "4",
        "blink": "5",
        "negative": "7",
        "crossed": "9",
    }

    light = None
    if len(color.split()) == 2:
        light, color = color.split()

    result = f'\033[{1 if light else 0};{colors.get(color.lower(), "")}m'
    for feature in features:
        if feature.lower() in colors.keys():
            result += f'\033[{colors[feature.lower()]}m'

    return result + str(text) + ("\033[0m" if reset else '')

def make_a_quote(quotes):
    random_quote = random.choice(quotes)
    words = random_quote.strip().split()
    formatted_quote = ""
    current_line = ""
    for word in words:
        if len(current_line.split()) + 1 > MAXSIGNLINE:
            formatted_quote += "\t" + current_line + "\n"
            current_line = ""
        current_line += word + " "
    formatted_quote += "\t" + current_line.strip()
    return formatted_quote

def create_problem_info(info, test, problem):
    problem_message = [
        problem,
        info['problems'][problem]['name'] if info['problems'][problem]['name'] != '' else '[No name]',
        info['problems'][problem]['status'],
        'c++' if info['problems'][problem]['lang'] == 'cpp' else 'python',
        f"{info['problems'][problem]['time_exceed']} Sec",
        f"{info['problems'][problem]['memory_exceed']} MB",
        f"{test['problems'][problem]['count']} test cases {test['problems'][problem]['type']} type" + (' by tester' if test['problems'][problem]['tester'] else ''),
    ]
    return problem_message

def create_max_field_widths(info, test):
    max_field_widths = {
        'problem_id': 0,  # Initialize maximum widths for each field
        'name': 0,
        'status': 0,
        'language': 0,
        'time_exceed': 0,
        'memory_exceed': 0,
        'test_cases': 0,
        'type': 0,
    }
    for problem in info['problems']:
        problem_message = create_problem_info(info, test, problem)
        for i, field in enumerate(problem_message):
            max_field_widths[list(max_field_widths)[i]] = max(max_field_widths[list(max_field_widths)[i]], len(field))
    return max_field_widths

def info():
    info = get_info()

    with open(os.path.join(PARSERDIR, 'testcase.json'), 'r') as infile:
        test = json.load(infile)

    print(f'Contest Name: {colored_text(info["name"], "light yellow")}')
    print(f'Description: {colored_text(info["description"], "light yellow") if info["description"] else colored_text("[No description]", "red")}')
    print(f'Link: {colored_text(info["link"], "light yellow") if info["link"] else colored_text("[No link]", "red")}')
    print(f'Number of Problems: {colored_text(info["num_problems"], "light yellow")}\n')

    status = {
        'out': 'light red',
        'raw': 'light gray',
        'stock': 'light magneta',
        'running': 'light yellow',
        'accept': 'light blue',
        'done': 'light green',
    }

    max_field_widths = create_max_field_widths(info, test)
    for problem in info['problems']:
        color = status[info['problems'][problem]['status']]
        problem_message = create_problem_info(info, test, problem)        
        sign_status = colored_text('signed', 'green') if info['problems'][problem]['sign'] else colored_text('no signed', 'red')
        formatted_message = ' - '.join(f"{field:{max_field_widths[key]}}" for key, field in zip(max_field_widths, problem_message))

        print(colored_text(formatted_message, color), '-', sign_status)

def open_problem(problem):
    info = get_info()
    if problem not in info['problems']:
        print(f'{colored_text("Error", "red")}: invalid problem name - {problem} not exist!')
        return
    if info['problems'][problem]['status'] == 'out':
        print(f'{colored_text("Error", "red")}: problem {problem} is on [out] mode (change it)')
        return
    runablefile = 'stock' if info['problems'][problem]['status'] == 'stock' else 'main'
    file = runablefile + '.' + info['problems'][problem]['lang']
    os.system(f'code {os.path.join(os.getcwd(), problem, file)}')

# ================================================================ initializer

def create_info_file(parser_address, name, signflag, lang, folder_names):
    problem_count = len(folder_names)
    problems = {}
    for folder_name in folder_names:
        problems[folder_name] = {
            "name": '',
            "status": "raw", # out (red), raw (gray), stock (magneta), running (yellow), accept (blue), done (green)
            "lang": lang,
            "time_exceed": 1.0,
            "memory_exceed": 256,
            'sign': 1 if signflag else 0
        }
    info = {
        "name": name,
        "description": "",
        "link": "",
        "num_problems": problem_count,
        'problems': problems,
    }
    
    with open(os.path.join(parser_address, 'info.json'), 'w') as info_file:
        json.dump(info, info_file, indent=4)

    if DEBUG:
        print(colored_text('info file created successfully!', 'green'))

def create_run_script(parser_address):
    script_content = f'''#!/bin/bash\n\npython3 "{__file__}" "$@"'''
    script_address = os.path.join(parser_address, 'r')
    with open(script_address, 'w') as f:
        f.write(script_content)
    os.chmod(script_address, 0o755)  # Add execute permissions to the script
    
    if DEBUG:
        print(colored_text('run scriptt file created successfully!', 'green'))

def sign_file(problem_name, info_address):

    with open(os.path.join(FILEDIR, 'sign.txt'), 'r') as sign_file:
        local_sign_content = sign_file.readlines()

    with open(os.path.join(FILEDIR, 'quotes.txt'), 'r') as quotes_file:
        quotes = quotes_file.readlines()
    
    with open(info_address, 'r') as infofile:
        info = json.load(infofile)

    original_name = info['problems'][problem_name]['name']
    problem_name_sign = problem_name if original_name == "" else f"{original_name} ({problem_name})"

    sign_content = ''
    sign_content += '/*\n' if info['problems'][problem_name]['lang'] == 'cpp' else '"""\n'
    sign_content += f'\tcontest name: {info["name"]}\n'
    sign_content += f'\tproblem name: {problem_name_sign}\n'
    sign_content += f'\tTime: {datetime.datetime.now().strftime("%Y-%m-%d %H:%M")}\n' # Time
    for line in local_sign_content:
        sign_content += f'\t{line}'
    sign_content += f'\n\n{make_a_quote(quotes)}\n'
    sign_content += '*/\n' if info['problems'][problem_name]['lang'] == 'cpp' else '"""\n'

    return sign_content

def name_problems(args):
    folder_names = []
    if args.problemnum:
        folder_names = [chr(ord('A') + i) for i in range(args.problemnum)]
    elif args.problemcustom:
        folder_names = args.problemcustom.upper().split()
    else:
        print(f'{colored_text("Error", "red")}: Enter num of qustion by [-problemnum] or [-problemcustom]')
        exit(1)
    return folder_names

def template_maker(contest_dir, problem_name, signflag, filename, template_content):
    problem_dir = os.path.join(contest_dir, problem_name)
    os.makedirs(problem_dir, exist_ok=True)
    
    with open(os.path.join(problem_dir, filename), 'w') as f:
        if signflag:
            f.write(sign_file(problem_name, os.path.join(contest_dir, '.parser', 'info.json')))
        f.write(template_content)

def folder_maker(folder_names, lang, signflag, contest_dir):
    os.makedirs(contest_dir, exist_ok=True)
    filename = 'main.cpp' if lang == 'cpp' else 'main.py'
    
    if lang == 'cpp':
        with open(os.path.join(FILEDIR, 'main.cpp'), 'r') as templatefile:
            template_content = templatefile.read()
    else:
        template_content = ''
    for problem_name in folder_names:
        template_maker(contest_dir, problem_name, signflag, filename, template_content)

def create_env(parser_dir, folder_names, name, signflag, lang):
    os.makedirs(parser_dir, exist_ok=True)
    samples_dir = os.path.join(parser_dir, 'samples')
    os.makedirs(samples_dir, exist_ok=True)
    for folder in folder_names:
        problem_dir = os.path.join(samples_dir, folder)
        os.makedirs(problem_dir, exist_ok=True)

def add_to_db(contest_dir):
    with open(os.path.join(FILEDIR, 'db.txt'), 'a') as db:
        db.write(f'{contest_dir}\n')

def initializer(args):
    name = args.initialize
    contest_dir = os.path.join(os.getcwd(), name)
    parser_dir = os.path.join(contest_dir, '.parser')
    lang = 'py' if args.language and args.language.lower() in ['python', 'py'] else 'cpp'
    signflag = args.sign != 'off' and args.env != 'off'

    if(os.path.exists(contest_dir)):
        print(f"{colored_text('Error', 'red')}: '{name}' already exists.")
        exit(1)

    folder_names = name_problems(args)
    
    if args.env != 'off':
        create_env(parser_dir, folder_names, name, signflag, lang)
        create_run_script(parser_dir)
        create_info_file(parser_dir, name, signflag, lang, folder_names)
        create_testcase_info(parser_dir, folder_names)
        if ADDTODB:
            add_to_db(contest_dir)
    
    folder_maker(folder_names, lang, signflag, contest_dir)

def addproblem(problem):
    info = get_info()
    if problem in info['problems']:
        print(f"{colored_text('Error', 'red')}: probelm {problem} already exist!")
        return
    with open(os.path.join(PARSERDIR, 'testcase.json'), 'r') as infile:
        test = json.load(infile)
    test['num_problems'] += 1
    info['num_problems'] += 1
    test['problems'][problem] = {
        'count': 0,
        'type': 'empty',
        'status': [],
        'tester': 0,
    }
    info['problems'][problem] = {
        "name": "",
        "status": "raw",
        "lang": "cpp",
        "time_exceed": 1.0,
        "memory_exceed": 256,
        "sign": 1
    }
    dump_info(info)
    with open(os.path.join(PARSERDIR, 'testcase.json'), 'w') as test_file:
        json.dump(test, test_file, indent=4)
    with open(os.path.join(FILEDIR, 'main.cpp'), 'r') as templatefile:
        template_content = templatefile.read()
    template_maker(os.getcwd(), problem, 1, 'main.cpp', template_content)
    os.makedirs(os.path.join(PARSERDIR, 'samples', problem), exist_ok=True)

def rmproblem(problem):
    info = get_info()
    if problem not in info['problems']:
        print(f"{colored_text('Error', 'red')}: probelm {problem} not find!")
        return
    with open(os.path.join(PARSERDIR, 'testcase.json'), 'r') as infile:
        test = json.load(infile)
    test['num_problems'] -= 1
    info['num_problems'] -= 1
    test['problems'].pop(problem)
    info['problems'].pop(problem)
    dump_info(info)
    with open(os.path.join(PARSERDIR, 'testcase.json'), 'w') as test_file:
        json.dump(test, test_file, indent=4)
    os.system(f'rm -r {os.path.join(os.getcwd(), problem)}')
    os.system(f'rm -r {os.path.join(PARSERDIR, "samples", problem)}')

# ========================================================== tester

def create_testcase_info(parser_dir, folder_name):
    empty_problem = {
        'count': 0,
        'type': 'empty',
        'status': [],
        'tester': 0,
    }
    problems = {}
    for name in folder_name:
        problems[name] = empty_problem
    testcase_info = {
        "num_problems": len(folder_name),
        "problems": problems,
    }
    with open(os.path.join(parser_dir, 'testcase.json'), 'w') as testcase_file:
        json.dump(testcase_info, testcase_file, indent=4)

def testcase_status():
    with open(os.path.join(PARSERDIR, 'testcase.json'), 'r') as file:
        test = json.load(file)
    print(f'num of problems: {colored_text(test["num_problems"], "light yellow")}\n')
    color = {
        'empty': 'red',
        'single': 'light green',
        'multi': 'light cyan',
    }
    for problem in test['problems']:
        count = test['problems'][problem]['count']
        message = problem + f" - {count} test case " + (f"{test['problems'][problem]['type']} mode" if count else '') + (f" - by tester" if test['problems'][problem]['tester'] else '')
        print(colored_text(message, color[test['problems'][problem]['type']]))
        
def testcase_update():
    jsonfile = os.path.join(PARSERDIR, 'testcase.json')
    with open(jsonfile, 'r') as infile:
        data = json.load(infile)
    for problem in data['problems']:
        sample_dir = os.path.join(PARSERDIR, 'samples', problem)
        if os.path.exists(os.path.join(sample_dir, 'test.in')) and os.path.exists(os.path.join(sample_dir, 'test.ans')):
            continue
        i = 1
        data['problems'][problem]['type'] = 'empty'
        pre_num = data['problems'][problem]['count']
        while os.path.exists(os.path.join(sample_dir, f'{i}.in')) and os.path.exists(os.path.join(sample_dir, f'{i}.ans')):
            i += 1
        i -= 1
        data['problems'][problem]['count'] = i
        if i:
            data['problems'][problem]['type'] = 'multi'
            if pre_num != i:
                print(colored_text(f"{i - pre_num} test case updated successfully in problem {problem}", "green"))

    with open(jsonfile, 'w') as outfile:
        json.dump(data, outfile, indent=4)

def testcase_reformat():
    with open(os.path.join(FILEDIR, 'formatio.txt'), 'r') as format_file:
        format_list = format_file.readlines()
    jsonfile = os.path.join(PARSERDIR, 'testcase.json')
    with open(jsonfile, 'r') as infile:
        data = json.load(infile)
    for format_io in format_list:
        input_pattern, output_pattern = format_io.strip().split()
        for problem in data['problems']:
            in_prefix, in_suffix = input_pattern.split('*')
            out_prefix, out_suffix = output_pattern.split('*')

            stanards = []
            i = 1
            while True:
                input_file = os.path.join(PARSERDIR, 'samples', problem, in_prefix + str(i) + in_suffix)
                output_file = os.path.join(PARSERDIR, 'samples', problem, out_prefix + str(i) + out_suffix)
                input_new = os.path.join(PARSERDIR, 'samples', problem, f'{i}.in')
                output_new = os.path.join(PARSERDIR, 'samples', problem, f'{i}.ans')
                if os.path.exists(input_file) and os.path.exists(output_file):
                    os.rename(input_file, input_new)
                    os.rename(output_file, output_new)
                    stanards.append(f'{i}.in')
                    stanards.append(f'{i}.ans')
                    i += 1
                else:
                    break
            i -= 1
            if i:
                for object in os.listdir(os.path.join(PARSERDIR, 'samples', problem)):
                    if object not in stanards:
                        os.system(f'rm -r {os.path.join(PARSERDIR, "samples", problem, object)}')
                break

def testcase_domjudge():
    with open(os.path.join(PARSERDIR, 'info.json'), 'r') as f:
        info = json.load(f)
    
    for problem in info['problems']:
        zip_file = os.path.join(PARSERDIR, 'samples', f'samples-{problem}.zip')
        target_folder = os.path.join(PARSERDIR, 'samples', problem)
        if os.path.exists(zip_file):
            with zipfile.ZipFile(zip_file, 'r') as zip_ref:
                zip_ref.extractall(target_folder)
            os.remove(zip_file)

def testcase_addformat():
    print('saved formats: ')
    with open(os.path.join(FILEDIR, 'formatio.txt'), 'r') as formatfile:
        saved = formatfile.readlines()
    for format in saved:
        i, o = format.split()
        print(colored_text(i, 'light magneta'), colored_text(o, 'light green'))
    print(colored_text('\nEnter formats. [* instead number][/ for directory seprate][empty for cancel]', 'light yellow'))
    input_format = input(colored_text('input format: ', 'light blue'))
    output_format = input(colored_text('output format: ', 'light blue'))
    if input_format and output_format:
        with open(os.path.join(FILEDIR, 'formatio.txt'), 'a') as formatfile:
            formatfile.write(f'{input_format} {output_format}\n')

def testcase_flush(problem, test):
    jsonfile = os.path.join(PARSERDIR, 'testcase.json')
    with open(jsonfile, 'r') as infile:
        data = json.load(infile)
    problem_folder = os.path.join(PARSERDIR, 'samples', problem)
    if(os.path.exists(problem_folder)):
        count = data['problems'][problem]['count']
        if test in ['all', '.']:
            try:
                os.system(f'rm -r {os.path.join(problem_folder, "*")}')
                data['problems'][problem]['type'] = 'empty'
                data['problems'][problem]['count'] = 0
                data['problems'][problem]['status'] = []
            except:
                print(f'{colored_text("Error", "red")}: we can\'t remove content of folder')
        elif data['problems'][problem]['type'] == 'multi' and count >= int(test) and int(test) > 0:
            os.remove(os.path.join(problem_folder, f'{test}.in'))
            os.remove(os.path.join(problem_folder, f'{test}.ans'))
            data['problems'][problem]['count'] -= 1
            for i in range(int(test), count):
                os.rename(os.path.join(problem_folder, f'{i + 1}.in'), os.path.join(problem_folder, f'{i}.in'))
                os.rename(os.path.join(problem_folder, f'{i + 1}.ans'), os.path.join(problem_folder, f'{i}.ans'))
            if data['problems'][problem]['count'] == 0:
                data['problems'][problem]['type'] = 'empty'
        else:
            print(f'{colored_text("Error", "red")}: test case not found [signle mode deleted by -test all]')
    else:
        print(f'{colored_text("Error", "red")}: problem not found')

    with open(jsonfile, 'w') as outfile:
        json.dump(data, outfile, indent=4)

def testcase_open(problem):
    try:
        if(problem in ['ALL', '.']):
            os.system(f"xdg-open '{os.path.join(PARSERDIR, 'samples')}'")
        else:
            os.system(f"xdg-open '{os.path.join(PARSERDIR, 'samples', problem)}'")
    except FileNotFoundError:
        print(f'{colored_text("Error", "red")}: invalid problem name - {problem} not exist!')

def input_testcase(message):
    print(colored_text(f'\nEnter {message}:', 'light cyan'))
    sections = []
    while True:
        section = input()
        if section == ENDTEST or section == '':
            break
        if section == CANCELTEST:
            return None
        if section == CANCELALL:
            exit(0)
        sections.append(section)
    return sections

def testcase_addmul_by_problem(problem, test):
    if test['problems'][problem]['type'] == 'single':
        print(f"{colored_text('Error', 'red')}: question {problem} have single mode test [flush it first]")
        return
    count = test['problems'][problem]['count']
    print(f"num of testcase question {problem} now: {colored_text(count, 'yellow')}")
    num = int(input(colored_text(f"Enter num of new Test case for question {problem}: ", 'light cyan')))
    for i in range(count + 1, num + count + 1):
        input_sections = input_testcase(f'input of test case num {i} question {problem}')
        if not input_sections:
            return
        output_sections = input_testcase(f'output of test case num {i} question {problem}')
        if not output_sections:
            return
        with open(os.path.join(PARSERDIR, 'samples', problem, f'{i}.in'), 'w') as f:
            f.write('\n'.join(input_sections))
        with open(os.path.join(PARSERDIR, 'samples', problem, f'{i}.ans'), 'w') as f:
            f.write('\n'.join(output_sections))
    if num:
        test['problems'][problem]['count'] = count + num
        test['problems'][problem]['type'] = 'multi'
    with open(os.path.join(PARSERDIR, 'testcase.json'), 'w') as f:
        json.dump(test, f, indent=4)

def testcase_addmul(problem):
    with open(os.path.join(PARSERDIR, 'testcase.json'), 'r') as file:
        test = json.load(file)
    if not problem or problem.upper() in ['.', 'ALL']:
        print(colored_text('Welcome to multi test case adder of all problems', 'light yellow'))
        print(colored_text(f'(cancel by {CANCELTEST} and ending by {ENDTEST} and exit test case adder by {CANCELALL})\n', 'yellow'))
        for problem in test['problems']:
            testcase_addmul_by_problem(problem, test)
    elif problem.upper() not in test['problems']:
        print(f"{colored_text('Error', 'red')}: {problem} not find!")
    else:
        print(colored_text(f'(cancel by {CANCELTEST} and ending by {ENDTEST} and exit test case adder by {CANCELALL})', 'yellow'))
        testcase_addmul_by_problem(problem.upper(), test)

def testcase_addsingle_by_problem(problem):
    input_sections = input_testcase(f'input of question {problem}')
    if not input_sections:
        return
    count_of_test = int(input_sections[0])
    num_of_lines_inputs = None
    if (len(input_sections) - 1) % count_of_test == 0:
        if input(colored_text(f'each input is {(len(input_sections) - 1) // count_of_test} line? (yes/no): ', 'yellow')).lower() in ['yes', 'y', '']:
            num_of_lines_inputs = [(len(input_sections) - 1) // count_of_test] * count_of_test
    if not num_of_lines_inputs or len(num_of_lines_inputs) != count_of_test:
        num_of_lines_inputs = list(map(int, input(colored_text(f'Enter {count_of_test} number: ', 'yellow')).strip().split()))
        if len(num_of_lines_inputs) == count_of_test - 1:
            num_of_lines_inputs.append(len(input_sections) - 1 - sum(num_of_lines_inputs))
    # ------------------------------------------------------------------ between input and output
    output_sections = input_testcase(f'output of question {problem}')
    if not output_sections:
        return
    num_of_lines_outputs = None
    if len(output_sections) % count_of_test == 0:
        if input(colored_text(f'each output is {len(output_sections) // count_of_test} line? (yes/no): ', 'yellow')).lower() in ['yes', 'y' , '']:
            num_of_lines_outputs = [len(output_sections) // count_of_test] * count_of_test
    while not num_of_lines_outputs or len(num_of_lines_outputs) != count_of_test:
        num_of_lines_outputs = list(map(int, input(colored_text(f'Enter {count_of_test} number: ', 'yellow')).strip().split()))
        if len(num_of_lines_outputs) == count_of_test - 1:
            num_of_lines_outputs.append(len(output_sections) - sum(num_of_lines_outputs))
    # ------------------------------------------------------------------ save information
    status = [(i, j) for i, j in zip(num_of_lines_inputs, num_of_lines_outputs)]
    testcase_file = os.path.join(PARSERDIR, 'testcase.json')
    with open(testcase_file, 'r') as file:
        test = json.load(file)
    test['problems'][problem] = {
        'count': count_of_test,
        'type': 'single',
        'status': status,
        'tester': test['problems'][problem]['tester']
    }
    # ------------------------------------------------------------------ write information
    with open(testcase_file, 'w') as f:
        json.dump(test, f, indent=4)
    with open(os.path.join(PARSERDIR, 'samples', problem, 'test.in'), 'w') as f:
        f.write('\n'.join(input_sections))
    with open(os.path.join(PARSERDIR, 'samples', problem, 'test.ans'), 'w') as f:
        f.write('\n'.join(output_sections))

def testcase_addsingle(problem):
    with open(os.path.join(PARSERDIR, 'testcase.json'), 'r') as file:
        test = json.load(file)
    if not problem or problem.upper() in ['.', 'ALL']:
        print(colored_text('Welcome to single test case adder of all problems', 'light yellow'))
        print(colored_text(f'(cancel by {CANCELTEST} and ending by {ENDTEST} and exit test case adder by {CANCELALL})\n', 'yellow'))
        for problem in test['problems']:
            testcase_addsingle_by_problem(problem)
    elif problem.upper() not in test['problems']:
        print(f"{colored_text('Error', 'red')}: {problem} not find!")
    else:
        print(colored_text(f'(cancel by {CANCELTEST} and ending by {ENDTEST} and exit test case adder by {CANCELALL})', 'yellow'))
        testcase_addsingle_by_problem(problem.upper())

def singlemode_show(problem, linestatus, showtogether):
    with open(os.path.join(PARSERDIR, 'samples', problem, 'test.in'), 'r') as f:
        input_sample = f.readlines()
    with open(os.path.join(PARSERDIR, 'samples', problem, 'test.ans'), 'r') as f:
        output_sample = f.readlines()
    if showtogether:
        print(colored_text('\nInput:', 'yellow'))
        print(''.join(input_sample))
        print(colored_text('Output:', 'yellow'))
        print(''.join(output_sample))
    else:
        input_sample = list(i.strip() for i in input_sample)
        output_sample = list(o.strip() for o in output_sample)
        cur_line_in = 1
        cur_line_out = 0
        for i, line in enumerate(linestatus, start=1):
            input_line, output_line = line[0], line[1]
            print(colored_text(f'\nTest case number {i}:', 'light cyan'))
            print(colored_text('input:', 'yellow'))
            for _ in range(input_line):
                print(input_sample[cur_line_in])
                cur_line_in += 1
            print(colored_text('output:', 'yellow'))
            for _ in range(output_line):
                print(output_sample[cur_line_out])
                cur_line_out += 1

def multimode_show(problem, count):
    for i in range(1, count + 1):
        print(colored_text(f'\nTest case number {i}:', 'light cyan'))
        print(colored_text('input:', 'yellow'))
        with open(os.path.join(PARSERDIR, 'samples', problem, f'{i}.in'), 'r') as f:
            print(''.join(f.readlines()))
        print(colored_text('output:', 'yellow'))
        with open(os.path.join(PARSERDIR, 'samples', problem, f'{i}.ans'), 'r') as f:
            print(''.join(f.readlines()))

def testcase_show(problem, showtogether):
    with open(os.path.join(PARSERDIR, 'testcase.json'), 'r') as file:
        test = json.load(file)
    if problem not in test['problems']:
        print(f"{colored_text('Error', 'red')}: {problem} not found!")
        return
    if test['problems'][problem]['type'] == 'empty':
        print(colored_text('Test case is empty!', 'red'))
        return
    print(f"\nType of testcase: {colored_text(test['problems'][problem]['type'], 'yellow')}")
    print(f"num of testcase: {colored_text(test['problems'][problem]['count'], 'yellow')}")
    if test['problems'][problem]['type'] == 'single':
        singlemode_show(problem, test['problems'][problem]['status'], showtogether)
    else:
        multimode_show(problem, test['problems'][problem]['count'])

def testcase_m2s(problem):
    with open(os.path.join(PARSERDIR, 'testcase.json'), 'r') as file:
        test = json.load(file)
    if problem not in test['problems']:
        print(f"{colored_text('Error', 'red')}: problem {problem} not found!")
        return    
    if test['problems'][problem]['type'] != 'multi':
        print(f"{colored_text('Error', 'red')}: problem {problem} is not multi mode for test case!")
        return
    input_path = os.path.join(PARSERDIR, 'samples', problem, '1.in')
    output_path = os.path.join(PARSERDIR, 'samples', problem, '1.ans')
    with open(input_path, 'r') as inputfile, open(output_path, 'r') as outputfile:
        input_sections = inputfile.readlines()
        output_sections = outputfile.readlines()
        input_sections = [i.strip() for i in input_sections]
        output_sections = [o.strip() for o in output_sections]
    if len(input_sections[0].split()) != 1:
        print(f"{colored_text('Error', 'red')}: test case is not in standard format!")
        return
    print(colored_text(f'Enter Information about problem {problem} test case:', 'cyan'))
    count_of_test = int(input_sections[0])
    num_of_lines_inputs = None
    if (len(input_sections) - 1) % count_of_test == 0:
        if input(colored_text(f'each input is {(len(input_sections) - 1) // count_of_test} line? (yes/no): ', 'yellow')).lower() in ['yes', 'y', '']:
            num_of_lines_inputs = [(len(input_sections) - 1) // count_of_test] * count_of_test
    if not num_of_lines_inputs or len(num_of_lines_inputs) != count_of_test:
        num_of_lines_inputs = list(map(int, input(colored_text(f'Enter {count_of_test} number: ', 'yellow')).strip().split()))
        if len(num_of_lines_inputs) == count_of_test - 1:
            num_of_lines_inputs.append(len(input_sections) - 1 - sum(num_of_lines_inputs))
    # ------------------------------------------------------------------ between input and output
    num_of_lines_outputs = None
    if len(output_sections) % count_of_test == 0:
        if input(colored_text(f'each output is {len(output_sections) // count_of_test} line? (yes/no): ', 'yellow')).lower() in ['yes', 'y' , '']:
            num_of_lines_outputs = [len(output_sections) // count_of_test] * count_of_test
    while not num_of_lines_outputs or len(num_of_lines_outputs) != count_of_test:
        num_of_lines_outputs = list(map(int, input(colored_text(f'Enter {count_of_test} number: ', 'yellow')).strip().split()))
        if len(num_of_lines_outputs) == count_of_test - 1:
            num_of_lines_outputs.append(len(output_sections) - sum(num_of_lines_outputs))
    # ------------------------------------------------------------------ save information
    status = [(i, j) for i, j in zip(num_of_lines_inputs, num_of_lines_outputs)]
    testcase_file = os.path.join(PARSERDIR, 'testcase.json')
    with open(testcase_file, 'r') as file:
        test = json.load(file)
    test['problems'][problem] = {
        'count': count_of_test,
        'type': 'single',
        'status': status,
        'tester': test['problems'][problem]['tester']
    }
    # ------------------------------------------------------------------ write information
    with open(testcase_file, 'w') as f:
        json.dump(test, f, indent=4)
    os.rename(input_path, os.path.join(PARSERDIR, 'samples', problem, 'test.in'))
    os.rename(output_path, os.path.join(PARSERDIR, 'samples', problem, 'test.ans'))
    print(colored_text(f'change problem {problem} test case from multi to single', 'green'))

def testcase_addtester(problem):
    testcase_file = os.path.join(PARSERDIR, 'testcase.json')
    with open(testcase_file, 'r') as file:
        test = json.load(file)
    if problem not in test['problems']:
        print(f"{colored_text('Error', 'red')}: problem {problem} not found!")
        return
    tester_path = os.path.join(PARSERDIR, 'samples', problem, 'test.py')
    if not os.path.exists(tester_path):
        with open(os.path.join(FILEDIR, 'tester.py'), 'r') as template, open(tester_path, 'w') as file:
            file.write(template.read())
    test['problems'][problem]['tester'] = 1
    with open(testcase_file, 'w') as f:
        json.dump(test, f, indent=4)
    os.system(f'code {tester_path}')

def testcase_rmtester(problem):
    testcase_file = os.path.join(PARSERDIR, 'testcase.json')
    with open(testcase_file, 'r') as file:
        test = json.load(file)
    if problem not in test['problems']:
        print(f"{colored_text('Error', 'red')}: problem {problem} not found!")
        return
    if test['problems'][problem]['tester'] == 0:
        print(f"{colored_text('Error', 'red')}: problem {problem} have not any tester!")
        return
    test['problems'][problem]['tester'] = 0
    with open(testcase_file, 'w') as f:
        json.dump(test, f, indent=4)
    print(colored_text(f'problem {problem} tester is off now', 'green'))

def testcase_ttt(problem):
    with open(os.path.join(PARSERDIR, 'testcase.json'), 'r') as file:
        test = json.load(file)
    if problem not in test['problems']:
        print(f"{colored_text('Error', 'red')}: problem {problem} not found!")
        return
    if test['problems'][problem]['tester'] == 0:
        print(f"{colored_text('Error', 'red')}: problem {problem} have not any tester!")
        return
    if test['problems'][problem]['type'] == 'empty':
        pass
    elif test['problems'][problem]['type'] == 'single':
        with open(os.path.join(PARSERDIR, 'samples', problem, 'test.ans'), 'r') as f:
                expected_output = f.read().strip()
        with open(os.path.join(PARSERDIR, 'samples', problem, 'test.in'), 'r') as f:
                expected_input = f.read().strip()
        expected_output = [o.strip() for o in expected_output.split('\n')]
        expected_input = [i.strip() for i in expected_input.split('\n')]
        output_line_cur = 0
        input_line_cur = 1
        for i, line in enumerate(test['problems'][problem]['status'], start=1):
            inputline, outputline = line[0], line[1]
            tester_path = os.path.join(PARSERDIR, 'samples', problem, 'test.py')
            spec = importlib.util.spec_from_file_location("tester", tester_path)
            testerfile = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(testerfile)
            try:
                result = testerfile.tester('\n'.join(expected_input[input_line_cur : input_line_cur + inputline]), '\n'.join(expected_output[output_line_cur : output_line_cur + outputline]))
            except Exception as err:
                result = f'{colored_text("err: ", "red")}{err}'
            output_line_cur += outputline
            input_line_cur += inputline
            # print(colored_text(f'Test Case number {i}:', 'yellow'), expected_output)
            print(colored_text(f'Test Case number {i}:', 'yellow'), result)
    else:
        for test_num in range(1, test['problems'][problem]['count'] + 1):
            input_test_path = os.path.join(PARSERDIR, 'samples', problem, f'{test_num}.in')
            output_test_path = os.path.join(PARSERDIR, 'samples', problem, f'{test_num}.ans')
            with open(output_test_path, 'r') as f:
                    expected_output = f.read().strip()
            with open(input_test_path, 'r') as f:
                    expected_input = f.read().strip()
            tester_path = os.path.join(PARSERDIR, 'samples', problem, 'test.py')
            spec = importlib.util.spec_from_file_location("tester", tester_path)
            testerfile = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(testerfile)
            try:
                result = testerfile.tester(expected_input, expected_output)
            except Exception as err:
                result = f'{colored_text("err: ", "red")}{err}'
            print(colored_text(f'Test Case number {i}:', 'yellow'), result)

# ========================================================== judge

def compile_code(problem_path, runablefile):
    run_command = ['g++', os.path.join(problem_path, f'{runablefile}.cpp'), '-o', os.path.join(problem_path, 'main')]
    process = subprocess.run(run_command, capture_output=True, text=True)  # Compile
    if process.returncode != 0:
        return {'status': 'compile error', 'output': process.stderr, 'error': None, 'execution_time': None, 'memory_usage': None}
    return {'status': 'success', 'output': None, 'error': None, 'execution_time': None, 'memory_usage': None}

def judge_code(problem_path, runablefile, lang, input_file, compile = True, run_flag = True):
    if compile and lang == 'cpp':
        compile_result = compile_code(problem_path, runablefile)
        if compile_result['status'] != 'success':
            return compile_result
    try:
        if run_flag:
            input_data = open(input_file, 'rb').read().decode('utf-8')
            start_memory = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
            start_time = timeit.default_timer()
            if lang == 'py':
                process = subprocess.run(['python3', os.path.join(problem_path, f'{runablefile}.py')], input=input_data, capture_output=True, text=True)
            else:
                if os.path.exists(os.path.join(problem_path, 'main')):
                    process = subprocess.run([os.path.join(problem_path, 'main')], input=input_data, capture_output=True, text=True)
                else:
                    print(f"{colored_text('Error', 'light red')}: main file not found (compile first)")
            end_time = timeit.default_timer()

            execution_time = end_time - start_time
            actual_output = process.stdout.strip()
            end_memory = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
            memory_usage = end_memory - start_memory

        return {'status': 'success', 'output': actual_output, 'error': None, 'execution_time': execution_time, 'memory_usage': memory_usage}

    except Exception as e:
        return {'status': 'error', 'output': None, 'error': str(e), 'execution_time': None, 'memory_usage': None}

def judge(args):
    info = get_info()
    with open(os.path.join(PARSERDIR, 'testcase.json'), 'r') as infile:
        test = json.load(infile)
    extrafile = args.judge.upper().split('/')
    problem = extrafile[0]
    if problem not in info['problems']:
        print(f'{colored_text("Error", "red")}: invalid problem name - {problem} not exist!')
        return
    if info['problems'][problem]['status'] == 'out':
        print(f'{colored_text("Error", "red")}: problem {problem} is on [out] mode (change it)')
        return
    if len(extrafile) == 1:
        runablefile = 'stock' if info['problems'][problem]['status'] == 'stock' else 'main'
        file = runablefile + '.' + info['problems'][problem]['lang']
        lang = info['problems'][problem]['lang']
    elif len(extrafile) == 2:
        file = extrafile[1].lower()
        if not os.path.exists(os.path.join(os.getcwd(), problem, file)):
            print(f"{colored_text('Error', 'red')}: {file} not find in problem {problem}!")
            return
        lang = 'cpp' if file.endswith('.cpp') else 'py'
        runablefile = file.split('.')[0]
    else:
        print(f"{colored_text('Error', 'red')}: invalid file path to judge [problem or problem/filename]")
    compile_flag = True

    if args.just:
        if args.just == 'compile':
            if lang == 'cpp':
                result = compile_code(os.path.join(os.getcwd(), problem), runablefile)
                if result['status'] == 'compile error':
                    print(f'{colored_text("Error", "light red")}:\n{result["output"]}')
                else:
                    message = f'question {problem} compiled successfully (file: {file})'
                    print(f"{colored_text(message, 'green')}")
                return
            else:
                print(f'{colored_text("Error", "light red")}: python file can not compile')
                return
        elif args.just == 'run':
            compile_flag = False
        else:
            print(f'{colored_text("Error", "light red")}: invalid argument for -just')
            return
    
    if args.test:
        if args.test != 'off':
            print(f'{colored_text("Error", "light red")}: invalid file name - {args.test} not exist!')
            return
        if lang == 'cpp':
            if compile_flag:
                result = compile_code(os.path.join(os.getcwd(), problem), runablefile)
                if result['status'] == 'compile error':
                    print(f'{colored_text("Error", "light red")}:\n{result["output"]}')
                    return
                else:
                    message = f'question {problem} compiled successfully'
                    print(f"{colored_text(message, 'green')}")
            if not os.path.exists(os.path.join(problem, 'main')):
                print(f"{colored_text('Error', 'light red')}: main file not found (compile first)")
                return
            print(f"{colored_text('program is running:', 'light cyan')}")
            os.system(os.path.join(problem, 'main'))
        else:
            filename = f'{runablefile}.py'
            print(f"{colored_text('program is running:', 'light cyan')}")
            os.system(f'python3 {os.path.join(problem, filename)}')
        return
    
    type_test = test['problems'][problem]['type']
    if type_test == 'empty':
        print(f'{colored_text("Error", "light red")}: test case of question {problem} is empty!')
        return
    if type_test == 'single':
        result = judge_code(os.path.join(os.getcwd(), problem), runablefile, lang, os.path.join(PARSERDIR, 'samples', problem, 'test.in'), compile=compile_flag)
        if result['status'] == 'error':
            print(f'{colored_text("Runtime Error", "light red")}:\n{result["error"]}')
            return
        with open(os.path.join(PARSERDIR, 'samples', problem, 'test.ans'), 'r') as f:
                expected_output = f.read().strip()
        with open(os.path.join(PARSERDIR, 'samples', problem, 'test.in'), 'r') as f:
                expected_input = f.read().strip()
        # print(f'output\n{result["output"]}')
        output = [o.strip() for o in result["output"].split('\n')]
        expected_output = [o.strip() for o in expected_output.split('\n')]
        expected_input = [i.strip() for i in expected_input.split('\n')]
        input_line_cur = 1
        output_line_cur = 0
        your_output_line_cur = 0
        desc = []
        total_status = True
        for i, line in enumerate(test['problems'][problem]['status'], start=1):
            input_line, outputline = line[0], line[1]
            if test['problems'][problem]['tester']:
                tester_path = os.path.join(PARSERDIR, 'samples', problem, 'test.py')
                spec = importlib.util.spec_from_file_location("tester", tester_path)
                testerfile = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(testerfile)
                try:
                    status_condition = testerfile.tester('\n'.join(expected_input[input_line_cur : input_line_cur + input_line]), '\n'.join(output[output_line_cur : output_line_cur + outputline]))
                except:
                    status_condition = False
            else:
                status_condition = output[output_line_cur : output_line_cur + outputline] == expected_output[output_line_cur : output_line_cur + outputline]
            if not status_condition:
                desc.append(f'incorrct in test case {i}')
                total_status = False
            status = colored_text('PASS', 'light green') if status_condition else colored_text('REJECT', 'light red')
            message = f'\nTest case num {i}:'
            print(f"{colored_text(message, 'light cyan')}", status)
            print(f"{colored_text('input:', 'yellow')}")
            for _ in range(input_line):
                print(expected_input[input_line_cur])
                input_line_cur += 1
            print(f"{colored_text('expected output:', 'yellow')}")
            for _ in range(outputline):
                print(expected_output[output_line_cur])
                output_line_cur += 1
            print(f"{colored_text('your output:', 'yellow')}")
            try:
                for _ in range(outputline):
                    print(output[your_output_line_cur])
                    your_output_line_cur += 1
            except IndexError:
                print(colored_text('your output is empty', 'red'))
            if test['problems'][problem]['tester']:
                print(f"{colored_text('tester result: ', 'magneta')}{colored_text('passed', 'green') if status_condition else colored_text('rejected', 'red')}")
        if args.timing and result["execution_time"] > info['problems'][problem]['time_exceed']:
            total_status = False
            desc.append('time exceeded')
        if args.memory and (result['memory_usage'] > info['problems'][problem]['memory_exceed'] * 1024 * 1024):
            total_status = False
            desc.append('memory exceeded')
        print(f'\nExecution Time: {colored_text((result["execution_time"]), "green" if "time exceeded" not in desc else "red")} sec')
        print(f'Memory usage: {colored_text((result["memory_usage"]), "green" if "memory exceeded" not in desc else "red")} bytes')
        status_message = colored_text('PASS', 'light green') if total_status else colored_text('REJECT', 'light red')
        print(colored_text(f'\ntotal status question {problem}:', 'yellow') , status_message)
        for m in desc:
            print(colored_text('err:', 'red'), m)
        info['problems'][problem]['status'] = 'accept' if total_status else 'running'

    else: # type_test == 'multi'
        total_status = True
        desc = []
        for test_num in range(1, test['problems'][problem]['count'] + 1):
            input_test_path = os.path.join(PARSERDIR, 'samples', problem, f'{test_num}.in')
            output_test_path = os.path.join(PARSERDIR, 'samples', problem, f'{test_num}.ans')
            result = judge_code(os.path.join(os.getcwd(), problem), runablefile, lang, input_test_path, compile=compile_flag)
            if result['status'] == 'error':
                print(f'{colored_text("Runtime Error", "light red")}:\n{result["error"]}')
                return
            elif result['status'] == 'compile error':
                print(f'{colored_text("Compile Error", "light red")}:\n{result["output"]}')
                return
            with open(output_test_path, 'r') as f:
                    expected_output = f.read().strip()
            with open(input_test_path, 'r') as f:
                    expected_input = f.read().strip()
            if test['problems'][problem]['tester']:
                tester_path = os.path.join(PARSERDIR, 'samples', problem, 'test.py')
                spec = importlib.util.spec_from_file_location("tester", tester_path)
                testerfile = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(testerfile)
                try:
                    status_condition = testerfile.tester(expected_input, result['output'])
                except:
                    status_condition = False
            else:
                status_condition = result['output'] == expected_output
            if not status_condition:
                desc.append(f'incorrct in test case {test_num}')
                total_status = False
            status = colored_text('PASS', 'light green') if status_condition else colored_text('REJECT', 'light red')
            message = f'\nTest case num {test_num}:'
            print(f"{colored_text(message, 'light cyan')}", status)
            if args.timing and result["execution_time"] > info['problems'][problem]['time_exceed']:
                total_status = False
                desc.append(f'time exceeded in test case {test_num}')
            if args.memory and (result['memory_usage'] > info['problems'][problem]['memory_exceed'] * 1024 * 1024):
                total_status = False
                desc.append(f'memory exceeded in test case {test_num}')
            print(f'Execution Time: {colored_text((result["execution_time"]), "green" if "time exceeded" not in desc else "red")} sec')
            print(f'Memory usage: {colored_text((result["memory_usage"]), "green" if "memory exceeded" not in desc else "red")} bytes')
            print(f"{colored_text('input:', 'yellow')}")
            print(expected_input)
            print(f"{colored_text('expected output:', 'yellow')}")
            print(expected_output)
            print(f"{colored_text('your output:', 'yellow')}")
            if result['output']:
                print(result['output'])
            else:
                print(colored_text('your output is empty', 'red'))
            if test['problems'][problem]['tester']:
                print(f"{colored_text('tester result: ', 'magneta')}{colored_text('passed', 'green') if status_condition else colored_text('rejected', 'red')}")
        status_message = colored_text('PASS', 'light green') if total_status else colored_text('REJECT', 'light red')
        print(colored_text(f'\ntotal status question {problem}:', 'yellow') , status_message)
        for m in desc:
            print(colored_text('err:', 'red'), m)
        info['problems'][problem]['status'] = 'accept' if total_status else 'running'

    if not runablefile == 'stock':
        with open(os.path.join(PARSERDIR, 'info.json'), 'w') as info_file:
            json.dump(info, info_file, indent=4)

# ========================================================== change

def dump_info(info):
    with open(os.path.join(PARSERDIR, 'info.json'), 'w') as info_file:
        json.dump(info, info_file, indent=4)

def get_info():
    with open(os.path.join(PARSERDIR, 'info.json'), 'r') as infile:
        info = json.load(infile)
    return info

def change_desc():
    info = get_info()
    print(colored_text(f'{EMPTY} for empty and Enter for Previous', 'magneta'))
    desc = input(colored_text("Enter a new description for contest: ", "yellow"))
    if desc:
        if desc == EMPTY:
            info['description'] = ""
        else:
            info['description'] = desc
    link = input(colored_text("Enter a new link for contest: ", "yellow"))
    if link:
        if desc == EMPTY:
            info['link'] = ""
        else:
            info['link'] = link
    choice = input(colored_text("Do you want to change problems name (yes/no): ", "blue"))
    if choice.lower() in ['yes', 'y']:
        for problem in info['problems']:
            name = input(colored_text(f'Enter new name for problem {problem}: ', 'yellow'))
            if name == EMPTY:
                info['problems'][problem]['name'] = ''
            elif name:
                info['problems'][problem]['name'] = name
    dump_info(info)

def change_time():
    print(colored_text('Welcome to time changer - Enter for Previous', 'magneta'))
    info = get_info()
    for problem in info['problems']:
        value = input(colored_text(f'Enter new Time of problem {problem} (sec): ', 'green'))
        if value:
            info['problems'][problem]['time_exceed'] = float(value)
    dump_info(info)

def change_memory():
    print(colored_text('Welcome to memory changer - Enter for Previous', 'magneta'))
    info = get_info()
    for problem in info['problems']:
        value = input(colored_text(f'Enter new Memory of problem {problem} (MB): ', 'green'))
        if value:
            info['problems'][problem]['memory_exceed'] = int(value)
    dump_info(info)

def change_status(problem, status):
    info = get_info()
    if problem not in info['problems']:
        print(f'{colored_text("Error", "red")}: invalid problem name - {problem} not exist!')
        return
    if status == info['problems'][problem]['status']:
        print(f'{colored_text("Error", "red")}: problem {problem} has already {status} status')
        return
    if status == 'out':
        info['problems'][problem]['status'] = 'out'
    elif status == 'stock':
        stock_path = os.path.join(os.getcwd(), problem, f"stock.{info['problems'][problem]['lang']}")
        if not os.path.exists(stock_path):
            with open(stock_path, 'w') as f:
                pass
        info['problems'][problem]['status'] = 'stock'
    elif status == 'raw':
        main_path = os.path.join(os.getcwd(), problem, f"main.{info['problems'][problem]['lang']}")
        if not os.path.exists(main_path):
            if info['problems'][problem]['lang'] == 'cpp':
                with open(os.path.join(FILEDIR, 'main.cpp'), 'r') as templatefile:
                    template_content = templatefile.read()
            else:
                template_content = ''
            template_maker(os.getcwd(), problem, info['problems'][problem]['sign'], f"main.{info['problems'][problem]['lang']}", template_content)
        info['problems'][problem]['status'] = 'raw'
    else:
        if info['problems'][problem]['status'] in ['out', 'stock']:
            print(f'{colored_text("Error", "red")}: problem {problem} has already {status} status. change it to [raw]')
            return
        if status in ['running', 'accept','done']:
            info['problems'][problem]['status'] = status
        else:
            print(f'{colored_text("Error", "red")}: invalid argument for -status [done | accept | running | raw | out | stock]')
            return
    dump_info(info)

def create_empty_code(info, lang, contest_dir, problem):
    if lang == 'cpp':
        with open(os.path.join(FILEDIR, 'main.cpp'), 'r') as templatefile:
            template_content = templatefile.read()
    else:
        template_content = ''
    template_maker(contest_dir, problem, info['problems'][problem]['sign'], f'main.{lang}', template_content)

def change_lang(problem, lang):
    info = get_info()
    if problem not in info['problems']:
        print(f'{colored_text("Error", "red")}: invalid problem name - {problem} not exist!')
        return
    if info['problems'][problem]['status'] in ['out', 'stock']:
        print(f'{colored_text("Error", "red")}: problem status is {info["problems"][problem]["status"]} (first change it)')
        return
    if lang not in ['cpp', 'c++', 'py', 'python']:
        print(f'{colored_text("Error", "red")}: {lang} language not exist!')
        return
    lang = 'cpp' if lang in ['cpp', 'c++'] else 'py'
    message = 'cpp' if lang in ['cpp', 'c++'] else 'python'
    if info['problems'][problem]['lang'] == lang:
        print(f'{colored_text("Error", "red")}: problem {problem} already is {message}')
        return
    info['problems'][problem]['lang'] = lang
    dump_info(info)

    if not os.path.exists(os.path.join(os.getcwd(), problem, f'main.{lang}')):
        create_empty_code(info, lang, os.getcwd(), problem)

def change_sign(problem, sign):
    info = get_info()
    if problem not in info['problems']:
        print(f'{colored_text("Error", "red")}: invalid problem name - {problem} not exist!')
        return
    if info['problems'][problem]['status'] in ['out', 'stock']:
        print(f'{colored_text("Error", "red")}: problem status is {info["problems"][problem]["status"]} (first change it)')
        return
    code_dir = os.path.join(os.getcwd(), problem, f"main.{info['problems'][problem]['lang']}")
    if sign == 'on':
        if info['problems'][problem]['sign']:
            print(f'{colored_text("Error", "red")}: sign for problem {problem} already is on')
            return
        with open(code_dir, 'r') as file:
            code = file.readlines()
        template_maker(os.getcwd(), problem, 1, f"main.{info['problems'][problem]['lang']}", ''.join(code))
        info['problems'][problem]['sign'] = 1
    elif sign == 'off':
        if not info['problems'][problem]['sign']:
            print(f'{colored_text("Error", "red")}: sign for problem {problem} already is off')
            return
        with open(code_dir, 'r') as file:
            code = file.readlines()
        sign_line = 1
        while sign_line < len(code):
            if code[sign_line].strip() in ['"""', '*/']:
                break
            sign_line += 1
        if sign_line == len(code):
            print(f'{colored_text("Error", "red")}: we have an error!')
        else:
            with open(code_dir, 'w') as file:
                file.write(''.join(code[sign_line + 1:]))
        info['problems'][problem]['sign'] = 0
    elif sign in ['rewrite', 're', 'resign']:
        if not info['problems'][problem]['sign']:
            print(f'{colored_text("Error", "red")}: sign for problem {problem} already is off')
            return
        with open(code_dir, 'r') as file:
            code = file.readlines()
        sign_line = 1
        while sign_line < len(code):
            if code[sign_line].strip() in ['"""', '*/']:
                break
            sign_line += 1
        if sign_line == len(code):
            print(f'{colored_text("Error", "red")}: we have an error!')
            info['problems'][problem]['sign'] = 0
        else:
            template_maker(os.getcwd(), problem, 1, f"main.{info['problems'][problem]['lang']}", ''.join(code[sign_line + 1:]))
    else:
        print(f'{colored_text("Error", "red")}: invalid argument for sign [on/off/rewrite]')
        return

    dump_info(info)

# ========================================================== ending

def delete_files_and_folders(directory, filename):
    for item in os.listdir(directory):
        item_path = os.path.join(directory, item)
        if os.path.isdir(item_path):
            delete_files_and_folders(item_path, filename)
            os.rmdir(item_path)
        else:
            if item != filename:
                os.remove(item_path)

def main_remover():
    for root, dirs, files in os.walk(os.getcwd()):
        for file in files:
            if file == "main":
                file_path = os.path.join(root, file)
                os.remove(file_path)

def etc_remover_for_problem(problem):
    folder_path = os.path.join(os.getcwd(), problem)
    info = get_info()
    if info['problems'][problem]['status'] == 'out':
        filename = None
    elif info['problems'][problem]['status'] == 'stock':
        filename = f'stock.{info["problems"][problem]["lang"]}'
    else:
        filename = f'main.{info["problems"][problem]["lang"]}'
    delete_files_and_folders(folder_path, filename)

def etc_remover(problem):
    info = get_info()
    if problem == 'ALL':
        for problem in info['problems']:
            etc_remover_for_problem(problem)
    elif problem in info['problems']:
        etc_remover_for_problem(problem)
    else:
        print(f'{colored_text("Error", "red")}: {problem} not found!')

def raw_remover():
    info = get_info()
    for problem in info['problems']:
        if info['problems'][problem]['status'] == 'raw':
                info['problems'][problem]['status'] = 'out'
    dump_info(info)

def create_markdown_for_problem(problem):
    info = get_info()
    with open(os.path.join(PARSERDIR, 'testcase.json'), 'r') as file:
        test = json.load(file)
    with open(os.path.join(os.getcwd(), problem, 'README.md'), 'w') as f:
        f.write(f'# problem {problem}')
        if info['problems'][problem]['name']:
            f.write(f' : {info["problems"][problem]["name"]}')
        lang = 'python' if info['problems'][problem]['lang'] == 'py' else 'c++'
        f.write(f'\n\nLanguage: {lang}\n\n')
        f.write(f'Time Exceed: {info["problems"][problem]["time_exceed"]} sec\n\n')
        f.write(f'Memory Exceed: {info["problems"][problem]["memory_exceed"]} MB\n\n')
        f.write(f'Number of Test Cases: {test["problems"][problem]["count"]}\n\n')
        if test['problems'][problem]['type'] == 'single':
            f.write('## Test Cases\n\n')
            with open(os.path.join(PARSERDIR, 'samples', problem, 'test.in'), 'r') as file:
                input_sample = file.readlines()
            with open(os.path.join(PARSERDIR, 'samples', problem, 'test.ans'), 'r') as file:
                output_sample = file.readlines()
            f.write('input:\n```\n')
            f.write(''.join(input_sample))
            f.write('\n```\n\n')
            f.write('output:\n```\n')
            f.write(''.join(output_sample))
            f.write('\n```\n\n')
        elif test['problems'][problem]['type'] == 'multi':
            f.write('## Test Cases\n\n')
            for i in range(1, test['problems'][problem]['count'] + 1):
                f.write(f'### Test Case {i}\n\n')
                with open(os.path.join(PARSERDIR, 'samples', problem, f'{i}.in'), 'r') as file:
                    input_sample = file.readlines()
                with open(os.path.join(PARSERDIR, 'samples', problem, f'{i}.ans'), 'r') as file:
                    output_sample = file.readlines()
                f.write('input:\n```\n')
                f.write(''.join(input_sample))
                f.write('\n```\n\n')
                f.write('output:\n```\n')
                f.write(''.join(output_sample))
                f.write('\n```\n\n')

def create_markdown():
    info = get_info()
    message = [
        f'# {info["name"]}\n\n',
    ]
    if info['description']:
        message.append(f"{info['description']}\n\n")
    if info['link']:
        message.append(f"Link: [{info['link']}]({info['link']})\n\n")
    message.append(f'writer: [{MYNAME}]({WEBSITE})\n\n')
    message.append(f'Email: [{EMAIL}](mailto:{EMAIL})\n\n')
    message.append(f'Number of Problems: {info["num_problems"]}\n\n')
    one_has_name = False
    for problem in info['problems']:
        if info['problems'][problem]['name']:
            one_has_name = True
            break
    if one_has_name:
        message.append('| | Name | Status | Language | Time Exceed | Memory Exceed |\n')
        message.append('|---|---|---|---|---|---|\n')
    else:
        message.append('| | Status | Language | Time Exceed | Memory Exceed |\n')
        message.append('|---|---|---|---|---|\n')
    for problem in info['problems']:
        if info['problems'][problem]['status'] == 'out':
            status = '`empty`'
        elif info['problems'][problem]['status'] == 'stock':
            status = 'other people'
        elif info['problems'][problem]['status'] == 'raw':
            status = 'raw file'
        elif info['problems'][problem]['status'] == 'running':
            status = 'reject'
        elif info['problems'][problem]['status'] == 'accept':
            status = 'accept test cases'
        elif info['problems'][problem]['status'] == 'done':
            status = 'Accept (100%)'
        lang = 'python' if info['problems'][problem]['lang'] == 'py' else 'c++'
        if one_has_name:
            problem_name = info['problems'][problem]['name'] if info['problems'][problem]['name'] else '`empty`'
            problem_name = f'[{problem_name}](./{problem}/)' if info['problems'][problem]['status'] != 'out' else f'{problem_name}'
            message.append(f'| [{problem}](./{problem}/) | {problem_name} | {status} | {lang} | {info["problems"][problem]["time_exceed"]} sec | {info["problems"][problem]["memory_exceed"]} MB |\n')
        else:
            message.append(f'| [{problem}](./{problem}/) | {status} | {lang} | {info["problems"][problem]["time_exceed"]} sec | {info["problems"][problem]["memory_exceed"]} MB |\n')
    with open(os.path.join(os.getcwd(), 'README.md'), 'w') as f:
        f.write(''.join(message))
    for problem in info['problems']:
        create_markdown_for_problem(problem)

# ========================================================== assets

def write_cpp_template(des, problem):
    with open(os.path.join(FILEDIR, 'main.cpp'), 'r') as templatefile:
        template_content = templatefile.read()
    with open(os.path.join(os.getcwd(), problem, des), 'w') as f:
        f.write(template_content)

def create_asset_code(des, src, problem, byetc):
    with open(os.path.join(FILEDIR, 'assets', src), 'r') as file:
        code = file.readlines()
    if src.endswith('.py') or src.endswith('.hpp') or byetc:
        content = code
    elif src.endswith('.cpp'):
        for i, line in enumerate(code):
            if 'using namespace std;' in line:
                header_end = i
            elif 'int main()' in line:
                main_start = i
        content = code[header_end + 1: main_start]
    else:
        print(f'{colored_text("Error", "red")}: invalid format [or use -byetc]!')
        return    
    des_list = des.split(':')
    if len(des_list) == 1:
        if des.isdigit():
            info = get_info()
            if info['problems'][problem]['status'] in ['out', 'stock']:
                print(f'{colored_text("Error", "red")}: problem {problem} is on [{info["problems"][problem]["status"]}] mode')
                return
            file = f'main.{info["problems"][problem]["lang"]}'
            with open(os.path.join(os.getcwd(), problem, file), 'r') as f:
                my_code = f.readlines()
            if len(my_code) < int(des):
                print(f'{colored_text("Error", "red")}: line {des} not found!')
                return
            with open(os.path.join(os.getcwd(), problem, file), 'w') as f:
                my_code.insert(int(des) - 1, ''.join(content))
                f.writelines(my_code)
        else:
            with open(os.path.join(os.getcwd(), problem, des), 'w') as f:
                f.write(''.join(content))
    elif len(des_list) == 2:
        if des_list[1].isdigit():
            if not os.path.exists(os.path.join(os.getcwd(), problem, des_list[0])):
                print(f'{colored_text("Error", "red")}: {des_list[0]} not found!')
                return
            with open(os.path.join(os.getcwd(), problem, des_list[0]), 'r') as f:
                my_code = f.readlines()
            if len(my_code) < int(des_list[1]):
                print(f'{colored_text("Error", "red")}: line {des_list[1]} not found!')
                return
            with open(os.path.join(os.getcwd(), problem, des_list[0]), 'w') as f:
                my_code.insert(int(des_list[1]) - 1, ''.join(content))
                f.writelines(my_code)
        else:
            print(f'{colored_text("Error", "red")}: invalid format!')
    else:
        print(f'{colored_text("Error", "red")}: invalid format!')

def print_assets(src_path, item):
    item_path = os.path.join(src_path, item)
    if os.path.isdir(item_path):
        return colored_text(item, 'yellow')
    elif item.endswith('.cpp'):
        return colored_text(item, 'green')
    elif item.endswith('.py'):
        return colored_text(item, 'cyan')
    elif item.endswith('.hpp'):
        return colored_text(item, 'magneta')
    else:
        return colored_text(item, 'red')

def choose_asset(src):
    print('')
    path = os.path.join(FILEDIR, 'assets', src)
    if os.path.isfile(path):
        return src
    items = list(reversed(os.listdir(path)))
    for i, item in enumerate(items, start=1):
        print(f"[{colored_text(i, 'red')}]", print_assets(path, item))
    while True:
        choice = input(colored_text(f"Enter a number between 0 (exit) to {len(items)}: ", 'yellow'))
        if not choice.isnumeric():
            print(f'{colored_text("Error", "red")}: invalid format!')
            continue
        choice = int(choice)
        if choice == 0:
            return None
        elif 0 < choice <= len(items):
            return choose_asset(os.path.join(src, items[choice - 1]))
        else:
            print(f'{colored_text("Error", "red")}: invalid number!')

def assets(des, src, problem, byetc = False):
    info = get_info()
    if problem not in info['problems']:
        print(f'{colored_text("Error", "red")}: problem {problem} not found!')
        return
    if src == 'main.cpp':
        write_cpp_template(des, problem)
    elif src == '+':
        src_path = choose_asset('.')
        if not src_path:
            return
        create_asset_code(des, src_path, problem, byetc)
        return
    src_path = os.path.join(FILEDIR, 'assets', src)
    if os.path.exists(src_path):
        if os.path.isdir(src_path):
            message = f'[{colored_text("directory", "yellow")}] [{colored_text("cpp files", "green")}]'
            message += f' [{colored_text("python files", "cyan")}] [{colored_text("hpp files", "magneta")}] [{colored_text("etc", "red")}]\n\n'
            message += f'{colored_text("directory [", "light blue", "underline")}{colored_text(src, "light green", "underline")}'
            message += colored_text("]:", "light blue", "underline")
            print(message)
            for item in reversed(os.listdir(src_path)):
                print(print_assets(src_path, item))
        else:
            create_asset_code(des, src, problem, byetc)
    else:
        print(f'{colored_text("Error", "red")}: {src} not found!')

# ========================================================== search

def find_by_name(name, problem):
    with open(os.path.join(FILEDIR, 'db.txt'), 'r') as file:
        db = file.readlines()
    db = [d.strip() for d in db]
    find_counter = 1
    while os.path.exists(os.path.join(os.getcwd(), problem, f'find-{find_counter}.cpp')) or os.path.exists(os.path.join(os.getcwd(), problem, f'find-{find_counter}.py')):
        find_counter += 1
    for address in db:
        if not address == os.getcwd():
            with open(os.path.join(address, '.parser', 'info.json'), 'r') as file:
                info = json.load(file)
            for p in info['problems']:
                if name.lower() in info['problems'][p]['name'].lower():
                    if info['problems'][p]['status'] in ['out', 'raw']:
                        message = colored_text('+ ', 'red')
                        message += colored_text(info['problems'][p]['name'], 'yellow')
                        print(f"{message} ({p} in {info['name']}) is found but it's {colored_text(info['problems'][p]['status'], 'red')}")
                    else:
                        message = colored_text('+ ', 'green')
                        message += colored_text(info['problems'][p]['name'], 'yellow')
                        message += f" ({p} in {info['name']}) is found ("
                        color_status = {
                            'stock': 'green', 'done': 'green', 'accept': 'cyan', 'running': 'yellow',
                        }
                        message += colored_text(info['problems'][p]['status'], color_status[info['problems'][p]['status']])
                        message += ') -> '
                        find_file = f"find-{find_counter}.{info['problems'][p]['lang']}"
                        message += colored_text(find_file, 'green')
                        main_name = f"{'stock' if info['problems'][p]['status'] == 'stock' else 'main'}.{info['problems'][p]['lang']}"
                        with open(os.path.join(address, p, main_name), 'r') as readfile, open(os.path.join(os.getcwd(), problem, find_file), 'w') as writefile:
                            writefile.write(readfile.read())
                        print(message)
                        find_counter += 1

def is_equal_just_test(list1_in, list1_out, list2_in, list2_out):
    for sample1_in, sample1_out in zip(list1_in, list1_out):
        for sample2_in, sample2_out in zip(list2_in, list2_out):
            if '\n'.join(sample1_in) == '\n'.join(sample2_in) and '\n'.join(sample1_out) == '\n'.join(sample2_out):
                return True
    return False

def is_equal_testcase(test_des, problem_des, path_des, test_src, problem_src):
    type_des = test_des['problems'][problem_des]['type']
    type_src = test_src['problems'][problem_src]['type']
    list1_in = []
    list1_out = []
    list2_in = []
    list2_out = []
    if type_des == 'empty':
        return False
    elif type_des == 'single':
        input_des = os.path.join(path_des, '.parser', 'samples', problem_des, 'test.in')
        output_des = os.path.join(path_des, '.parser', 'samples', problem_des, 'test.ans')
        with open(input_des, 'r') as ifile, open(output_des, 'r') as ofile:
            input_sample = ifile.readlines()
            output_sample = ofile.readlines()
            input_sample = [i.strip() for i in input_sample]
            output_sample = [o.strip() for o in output_sample]
        cur_line_input = 1
        cur_line_output = 0
        for lines in test_des['problems'][problem_des]['status']:
            input_line, output_line = lines[0], lines[1]
            list1_in.append(input_sample[cur_line_input: cur_line_input + input_line])
            list1_out.append(input_sample[cur_line_output: cur_line_output + output_line])
    else:
        for counter in range(1, test_des['problems'][problem_des]['count'] + 1):
            input_des = os.path.join(path_des, '.parser', 'samples', problem_des, f'{counter}.in')
            output_des = os.path.join(path_des, '.parser', 'samples', problem_des, f'{counter}.ans')
            with open(input_des, 'r') as ifile, open(output_des, 'r') as ofile:
                input_sample = ifile.readlines()
                output_sample = ofile.readlines()
                input_sample = [i.strip() for i in input_sample]
                output_sample = [o.strip() for o in output_sample]
            list1_in.append(input_sample)
            list1_out.append(output_sample)
    if type_src == 'single':
        input_src = os.path.join(PARSERDIR, 'samples', problem_src, 'test.in')
        output_src = os.path.join(PARSERDIR, 'samples', problem_src, 'test.ans')
        with open(input_src, 'r') as ifile, open(output_src, 'r') as ofile:
            input_sample = ifile.readlines()
            output_sample = ofile.readlines()
            input_sample = [i.strip() for i in input_sample]
            output_sample = [o.strip() for o in output_sample]
        cur_line_input = 1
        cur_line_output = 0
        for lines in test_src['problems'][problem_src]['status']:
            input_line, output_line = lines[0], lines[1]
            list2_in.append(input_sample[cur_line_input: cur_line_input + input_line])
            list2_out.append(input_sample[cur_line_output: cur_line_output + output_line])
    else:
        for counter in range(1, test_src['problems'][problem_src]['count'] + 1):
            input_src = os.path.join(PARSERDIR, 'samples', problem_src, f'{counter}.in')
            output_src = os.path.join(PARSERDIR, 'samples', problem_src, f'{counter}.ans')
            with open(input_src, 'r') as ifile, open(output_src, 'r') as ofile:
                input_sample = ifile.readlines()
                output_sample = ofile.readlines()
                input_sample = [i.strip() for i in input_sample]
                output_sample = [o.strip() for o in output_sample]
            list2_in.append(input_sample)
            list2_out.append(output_sample)
    return is_equal_just_test(list1_in, list1_out, list2_in, list2_out)

def find_by_io(problem):
    with open(os.path.join(FILEDIR, 'db.txt'), 'r') as file:
        db = file.readlines()
    db = [d.strip() for d in db]
    with open(os.path.join(PARSERDIR, 'testcase.json'), 'r') as file:
        my_test = json.load(file)
    if my_test['problems'][problem]['type'] == 'empty':
        print(colored_text(f'problem {problem} test case is empty!', 'red'))
        return
    find_counter = 1
    while os.path.exists(os.path.join(os.getcwd(), problem, f'find-{find_counter}.cpp')) or os.path.exists(os.path.join(os.getcwd(), problem, f'find-{find_counter}.py')):
        find_counter += 1
    for address in db:
        if not address == os.getcwd():
            with open(os.path.join(address, '.parser', 'info.json'), 'r') as file:
                info = json.load(file)
            with open(os.path.join(address, '.parser', 'testcase.json'), 'r') as file:
                test = json.load(file)
            for p in info['problems']:
                if is_equal_testcase(test , p, address, my_test, problem):
                    if info['problems'][p]['status'] in ['out', 'raw']:
                        message = colored_text('+ ', 'red')
                        message += colored_text(info['problems'][p]['name'], 'yellow')
                        print(f"{message} ({p} in {info['name']}) is found but it's {colored_text(info['problems'][p]['status'], 'red')}")
                    else:
                        message = colored_text('+ ', 'green')
                        message += colored_text(info['problems'][p]['name'], 'yellow')
                        message += f" ({p} in {info['name']}) is found ("
                        color_status = {
                            'stock': 'green', 'done': 'green', 'accept': 'cyan', 'running': 'yellow',
                        }
                        message += colored_text(info['problems'][p]['status'], color_status[info['problems'][p]['status']])
                        message += ') -> '
                        find_file = f"find-{find_counter}.{info['problems'][p]['lang']}"
                        message += colored_text(find_file, 'green')
                        main_name = f"{'stock' if info['problems'][p]['status'] == 'stock' else 'main'}.{info['problems'][p]['lang']}"
                        with open(os.path.join(address, p, main_name), 'r') as readfile, open(os.path.join(os.getcwd(), problem, find_file), 'w') as writefile:
                            writefile.write(readfile.read())
                        print(message)
                        find_counter += 1

def search(arg, problem):
    with open(os.path.join(PARSERDIR, 'info.json'), 'r') as file:
        info = json.load(file)
    if problem not in info['problems']:
        print(f"{colored_text('Error', 'red')}: problem {problem} not find!")
        return
    if arg.lower() == 'ioall':
        for p in info['problems']:
            find_by_io(p)
    elif arg.lower() == 'io':
        find_by_io(problem)
    else:
        find_by_name(arg, problem)

# ========================================================== main

help_message = [
    f"{colored_text('[-initialize|-i]', 'yellow')} {colored_text('[-CONTEST_NAME]', 'cyan')} {colored_text('[-problemnum][-problemcustom]', 'yellow')} {colored_text('[NUM_OR_NAMES]', 'cyan')} {colored_text('[-env]', 'yellow')} {colored_text('[off]', 'cyan')}",
    f"{colored_text('[-testcase|-t]', 'yellow')} {colored_text('[status][show][addmul][addsingle|adds][update][reformat][addformat][flush][domjudge]', 'green')}",
    f"{colored_text('[-testcase|-t]', 'yellow')} {colored_text('[multitosingle|m2s][opendir][addtester][removetester|rmtester][testtester|ttt]', 'green')}",
    f"{colored_text('[-info]', 'yellow')}",
    f"{colored_text('[-change]', 'yellow')} {colored_text('[-timing|-time][-memory][-status][-language|-lang][-sign][-contest]', 'yellow')}",
    f"{colored_text('[-problem|-p]', 'yellow')} {colored_text('[PROBLEMNAME]', 'cyan')}",
    f"{colored_text('[-ending|-end]', 'yellow')} {colored_text('[removemain|rmmain][removeetc|rmetc][removeraw|rmraw][markdown|md]', 'green')}",
    f"{colored_text('[-search]', 'yellow')} {colored_text('[NAME|', 'cyan')}{colored_text('io|ioall]', 'green')}",
    f"{colored_text('[-asset|-as]', 'yellow')} {colored_text('[DESTINATION_FILE_LINE_OR_BOTH-(temp.cpp:32)]', 'cyan')} {colored_text('[SRC|+]', 'cyan')} {colored_text('[-p|-problem]', 'yellow')} {colored_text('[PROBLEMNAME]', 'cyan')}",
]


def main():
    parser = argparse.ArgumentParser(description='commands of parser information')
    parser.add_argument('-initialize', '-i' , metavar='name', type=str, help='contest name')
    parser.add_argument('-problemnum', metavar='NUM_PROBLEMS', type=int, help='Number of problems to implement')
    parser.add_argument('-problemcustom', metavar='NAME_PROBLEMS', type=str, help='name of problems to implement')
    parser.add_argument('-env', metavar='environment', type=str, help='name of problems to implement')
    parser.add_argument('-info', action='store_true', help='Show information about the competition')
    parser.add_argument('-testcase', '-t', metavar='testcase', type=str, help='about out test cases')
    parser.add_argument('-problem', '-p', metavar='problem', type=str, help='choose a problem')
    parser.add_argument('-test', metavar='test', type=str, help='choose a testcase')
    parser.add_argument('-sign', metavar='sign', type=str, help='sign of the problem')
    parser.add_argument('-language', '-lang', metavar='language', type=str, help='sign of the problem')
    parser.add_argument('-judge', '-j', metavar='judge', type=str, help='judge the problem')
    parser.add_argument('-just', metavar='just', type=str, help='just something [compile | run]')
    parser.add_argument('-timing', '-time', action='store_true', help='by time or not')
    parser.add_argument('-memory', action='store_true', help='by memory used or not')
    parser.add_argument('-change', action='store_true', help='change something')
    parser.add_argument('-contest', action='store_true', help='about contest [description]')
    parser.add_argument('-status', metavar='status', type=str, help='you should choose: [out | raw | stock | running | accept | done]')
    parser.add_argument('-ending', '-end', metavar='ending', type=str, help='for end of contest')
    parser.add_argument('-assets', '-as', nargs=2, metavar=("des", "src") , type=str, help='assets codes')
    parser.add_argument('-byetc', action='store_true', help='by etc or not')
    parser.add_argument('-search', metavar='search', type=str, help='for end of contest')
    parser.add_argument('-addproblem', '-addp', metavar='addproblem', type=str, help='to add a problem')
    parser.add_argument('-rmproblem', '-rmp', metavar='addproblem', type=str, help='to remove a problem')
    args = parser.parse_args()

    if args.initialize:
        initializer(args)
    elif args.info:
        info()
    elif args.judge:
        judge(args)
    elif args.addproblem:
        addproblem(args.addproblem.upper())
    elif args.rmproblem:
        rmproblem(args.rmproblem.upper())
    elif args.testcase:
        if args.testcase == 'update':
            testcase_update()
        elif args.testcase == 'domjudge':
            testcase_domjudge()
            testcase_update()
        if args.testcase == 'status':
            testcase_status()
        elif args.testcase == 'reformat':
            testcase_reformat()
            testcase_update()
        elif args.testcase == 'addformat':
            testcase_addformat()
        elif args.testcase == 'opendir':
            if args.problem == None:
                problem = 'ALL'
            else:
                problem = args.problem.upper()
            testcase_open(problem)
        elif args.testcase == 'flush':
            if args.problem == None:
                print(f'{colored_text("Error", "red")}: Please provide a problem name.')
                return
            elif args.test == None:
                test = 'all'
            else:
                test = args.test.lower()
            testcase_flush(args.problem.upper(), test)
        elif args.testcase in ['addsingle', 'adds']:
            testcase_addsingle(args.problem)
        elif args.testcase == 'addmul':
            testcase_addmul(args.problem)
        elif args.testcase == 'show':
            if args.problem == None:
                print(f'{colored_text("Error", "red")}: Please provide a problem name.')
                return
            testcase_show(args.problem.upper(), args.test and args.test.lower() in ['all', '.'])
        elif args.testcase in ['multitosingle', 'm2s']:
            if args.problem == None:
                print(f'{colored_text("Error", "red")}: Please provide a problem name.')
                return
            testcase_m2s(args.problem.upper())
        elif args.testcase == 'addtester':
            if args.problem == None:
                print(f'{colored_text("Error", "red")}: Please provide a problem name.')
                return
            testcase_addtester(args.problem.upper())
        elif args.testcase in ['removetester', 'rmtester']:
            if args.problem == None:
                print(f'{colored_text("Error", "red")}: Please provide a problem name.')
                return
            testcase_rmtester(args.problem.upper())
        elif args.testcase in ['testtester', 'ttt']:
            if args.problem == None:
                print(f'{colored_text("Error", "red")}: Please provide a problem name.')
                return
            testcase_ttt(args.problem.upper())
        else:
            print(f"{colored_text('Error', 'red')}: invalid input for -testcase")
    elif args.change:
        if args.contest:
            change_desc()
        elif args.timing:
            change_time()
        elif args.memory:
            change_memory()
        else:
            if args.problem == None:
                print(f"{colored_text('Error', 'red')}: you should choose a problem by -p")
                return
            if args.status:
                change_status(args.problem.upper(), args.status.lower())
            elif args.language:
                change_lang(args.problem.upper(), args.language.lower())
            elif args.sign:
                change_sign(args.problem.upper(), args.sign.lower())
            else:
                print(f"{colored_text('Error', 'red')}: you should change something!")
    elif args.ending:
        if args.ending in ['removemain', 'rmmain']:
            main_remover()
        elif args.ending in ['markdown', 'md']:
            create_markdown()
        elif args.ending in ['removeetc' , 'rmetc']:
            if not args.problem or args.problem.upper() in ['.', 'ALL']:
                problem = 'ALL'
            else:
                problem = args.problem.upper()
            etc_remover(problem)
        elif args.ending in ['removeraw', 'rmraw']:
            raw_remover()
        else:
            print(f"{colored_text('Error', 'red')}: invalid argument for -ending")
    elif args.assets:
        if args.problem == None:
            print(f"{colored_text('Error', 'red')}: you should choose a problem by -p")
            return
        if args.byetc:
            assets(args.assets[0], args.assets[1], args.problem.upper(), True)
        else:
            assets(args.assets[0], args.assets[1], args.problem.upper())
    elif args.search:
        if args.problem == None:
            print(f"{colored_text('Error', 'red')}: you should choose a problem by -p")
            return
        search(args.search, args.problem.upper())
    elif args.problem:
        open_problem(args.problem.upper())
    else:
        print('\n'.join(help_message))


if __name__ == "__main__":
    main()


""" Help message

    -initialize [CONTEST_NAME]: create a new competition directory with the given name and problems
    -problemnum: number of problems to implement
    -problemcustom: name of problems to implement
    -env [off]: create a parser environment in the competition directory
    -info | -i : show information about the competition

    -testcase: about out test cases
       status: show the status of the test cases
       update: update the test cases
       reformat: reformat the test cases
       addformat: add format to the test cases
       opendir: open the test cases folder
       flush: flush the test cases
       addsingle: add single test case
       addmulti: add multi test case
        domjudge: reformat domjudge test case by zip file
       show: showing test case
        m2s: multi to single
    -test | -t : choose a testcase
    -problem | -p : choose a problem

    -judge | -j : judge the code
    -timing: show the time of the code
    -just [compile | run]: just compile or run the code
    -test | -t [off]: without test
    *note: this argument does not need to -problem args
    
    -change : change the code
    -problem | -p : choose a problem
    -language | -lang : new language to choose
    -status [done | accept | running | raw | out | stock]: new status to choose
    -timing: new time to choose
    -memory: new memory to choose
    -sign [on | off | rewrite]: sign of the problem
    -contest: adding descrition and link of the contest

    -ending: ending the competition
        markdown: create a markdown file of the contest
        removeraw: remove the raw status of the problem to out status
        removemain: remove the main file of the problems
        removeetc: remove the etc files of the problems except the main code
    
    -assets: create a assets code for the contest
       [line to add | file to add(by line or without)] [address of asset | main.cpp (template)]
       -byetc: adding header and main func too

    -search:
        io-base
        other

"""