import os
import argparse
import json
import random
import datetime

MAXSIGNLINE = 20
ENDTEST = 'ENDTEST'
CANCELTEST = 'CANCELTEST'
FILEDIR = os.path.dirname(__file__)
PARSERDIR = os.path.join(os.getcwd(), '.parser')

def colored_text(text, color):
    colors = {
        'reset': '\033[0m',
        'black': '\033[30m',
        'red': '\033[31m',
        'green': '\033[32m',
        'yellow': '\033[33m',
        'blue': '\033[34m',
        'magenta': '\033[35m',
        'cyan': '\033[36m',
        'white': '\033[37m'
    }
    return colors.get(color.lower(), '') + str(text) + colors['reset']

# ================================================================ initializer

# def print_competition_info():
#     parser_dir = os.path.join(os.getcwd(), '.parser')
#     info_file_path = os.path.join(parser_dir, 'info.json')

#     if os.path.exists(info_file_path):
#         with open(info_file_path, 'r') as info_file:
#             info = json.load(info_file)
#             print("Competition Name:", colored_text(info.get("contest_name"), "green"))
#             print("Number of Problems:", colored_text(info.get("num_problems"), "green"))
#             samples_status = info.get("samples_state")
#             if samples_status == "empty":
#                 samples_status = colored_text(info.get("samples_state"), "red")
#             print("Samples State:", samples_status)
#     else:
#         print(f"{colored_text('Error', 'red')}: You are not in a competition directory or info file is missing.")

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

def create_run_script(parser_address):
    script_content = f'''#!/bin/bash\n\npython3 "{__file__}" "$@"'''
    script_address = os.path.join(parser_address, 'r')
    with open(script_address, 'w') as f:
        f.write(script_content)
    os.chmod(script_address, 0o755)  # Add execute permissions to the script

def initializer(args):
    name = args.initialize
    folder_names = []
    if args.problemnum:
        folder_names = [chr(ord('A') + i) for i in range(args.problemnum)]
    elif args.problemcustom:
        folder_names = args.problemcustom.upper().split()
    else:
        print(f'{colored_text("Error", "red")}: Enter num of qustion by [-problemnum] or [-problemcustom]')
        return

    problem_count = len(folder_names)
    lang = 'py' if args.language and args.language.lower() in ['python', 'py'] else 'cpp'
    filename = 'main.cpp' if lang == 'cpp' else 'main.py'
    signflag = args.sign != 'off'

    if lang == 'cpp':
        with open(os.path.join(FILEDIR, 'main.cpp'), 'r') as templatefile:
            template_content = templatefile.read()
    else:
        template_content = ''

    with open(os.path.join(FILEDIR, 'sign.txt'), 'r') as sign_file:
        sign_content = sign_file.readlines()

    with open(os.path.join(FILEDIR, 'quotes.txt'), 'r') as quotes_file:
        quotes = quotes_file.readlines()

    contest_dir = os.path.join(os.getcwd(), name)
    if(os.path.exists(contest_dir)):
        print(f"{colored_text('Error', 'red')}: '{name}' already exists.")
        return
    os.makedirs(contest_dir, exist_ok=True)

    for problem_name in folder_names:
        problem_dir = os.path.join(contest_dir, problem_name)
        os.makedirs(problem_dir, exist_ok=True)
        
        with open(os.path.join(problem_dir, filename), 'w') as f:
            if signflag:
                f.write('"""\n') if lang == 'py' else f.write('/*\n')
                if type != 'question' and type != 'q':
                    f.write(f'\tcontest name: {name}\n')
                f.write(f'\tproblem name: {problem_name}\n')
                f.write(f'\tTime: {datetime.datetime.now().strftime("%Y-%m-%d %H:%M")}\n') # Time
                for sign_line in sign_content:
                    f.write(f'\t{sign_line}')
                f.write(f'\n\n{make_a_quote(quotes)}\n')
                f.write('"""\n\n') if lang == 'py' else f.write('*/\n\n')
            f.write(template_content)

    if args.env != 'off':
        parser_dir = os.path.join(contest_dir, '.parser')
        os.makedirs(parser_dir, exist_ok=True)
        create_run_script(parser_dir)
        samples_dir = os.path.join(parser_dir, 'samples')
        os.makedirs(samples_dir, exist_ok=True)

        for folder in folder_names:
            problem_dir = os.path.join(samples_dir, folder)
            os.makedirs(problem_dir, exist_ok=True)

        info = {
            "name": name,
            "num_problems": problem_count,
            "sign_state": [1 if signflag else 0] * problem_count,
            "folder_names": folder_names,
            "problem_names": [None] * problem_count,
            "time_exceed": [1.0] * problem_count,
            "memory_exceed": [256] * problem_count,
        }
        with open(os.path.join(parser_dir, 'info.json'), 'w') as info_file:
            json.dump(info, info_file, indent=4)
        create_testcase_info(parser_dir, folder_names)

# ========================================================== tester

def modify_json(file, problem_id, count, problem_type, status):
    with open(file, 'r') as infile:
        data = json.load(infile)

    if problem_id not in data['problems']:
        return False
    
    data['problems'][problem_id] = {
        'count': count,
        'type': problem_type,
        'status': status if status else []
    }

    with open(file, 'w') as outfile:
        json.dump(data, outfile, indent=4)

def create_testcase_info(parser_dir, folder_name):
    empty_problem = {
        'count': 0,
        'type': 'empty',
        'status': [],
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
    pass

def testcase_update():
    jsonfile = os.path.join(PARSERDIR, 'testcase.json')
    with open(jsonfile, 'r') as infile:
        data = json.load(infile)
    for problem in data['problems'].keys():
        sample_dir = os.path.join(PARSERDIR, 'samples', problem)
        if os.path.exists(os.path.join(sample_dir, 'test.in')) and os.path.exists(os.path.join(sample_dir, 'test.ans')):
            continue
        i = 1
        data['problems'][problem]['type'] = 'empty'
        while os.path.exists(os.path.join(sample_dir, f'{i}.in')) and os.path.exists(os.path.join(sample_dir, f'{i}.ans')):
            i += 1
        i -= 1
        data['problems'][problem]['count'] = i
        if i:
            data['problems'][problem]['type'] = 'multi'
            print(colored_text(f"{i} test case updated successfully in problem {problem}", "green"))

    with open(jsonfile, 'w') as outfile:
        json.dump(data, outfile, indent=4)

def testcase_refactor():
    with open(os.path.join(FILEDIR, 'formatio.txt'), 'r') as format_file:
        format_list = format_file.readlines()
    jsonfile = os.path.join(PARSERDIR, 'testcase.json')
    with open(jsonfile, 'r') as infile:
        data = json.load(infile)
    for format_io in format_list:
        input_pattern, output_pattern = format_io.strip().split()
        for problem in data['problems'].keys():
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
                data['problems'][problem]['count'] = i
                data['problems'][problem]['type'] = 'multi'
                print(colored_text(f"{i} test case updated successfully in problem {problem}", "green"))
                for object in os.listdir(os.path.join(PARSERDIR, 'samples', problem)):
                    if object not in stanards:
                        os.system(f'rm -r {os.path.join(PARSERDIR, "samples", problem, object)}')
                break
    with open(jsonfile, 'w') as outfile:
        json.dump(data, outfile, indent=4)


def testcase_addformat():
    pass

def testcase_rewrite(problem):
    pass

def testcase_flush(problem, test):
    jsonfile = os.path.join(PARSERDIR, 'testcase.json')
    with open(jsonfile, 'r') as infile:
        data = json.load(infile)
    problem_folder = os.path.join(PARSERDIR, 'samples', problem)
    if(os.path.exists(problem_folder)):
        count = data['problems'][problem]['count']
        if test == 'all':
            try:
                os.system(f'rm -r {os.path.join(problem_folder, "*")}')
                data['problems'][problem]['type'] = 'empty'
                data['problems'][problem]['count'] = 0
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
            print(f'{colored_text("Error", "red")}: test case not found')
    else:
        print(f'{colored_text("Error", "red")}: problem not found')

    with open(jsonfile, 'w') as outfile:
        json.dump(data, outfile, indent=4)

def testcase_open(problem):
    try:
        if(problem == 'ALL'):
            os.system(f"xdg-open '{os.path.join(PARSERDIR, 'samples')}'")
        else:
            os.system(f"xdg-open '{os.path.join(PARSERDIR, 'samples', problem)}'")
    except FileNotFoundError:
        print(f'{colored_text("Error", "red")}: invalid problem name - {problem} not exist!')

def testcase_addmul(problem):
    pass

def testcase_addsingle(problem):
    print(colored_text(f'Enter input of question {problem} (cancel by CANCELTEST and ending by ENDTEST):', 'yellow'))
    input_sections = []
    while True:
        section = input()
        if section == ENDTEST:
            break
        if section == CANCELTEST:
            return
        input_sections.append(section)
    num_of_lines_inputs = list(map(int, input(f'Eenter {input_sections[0]} number: ').strip().split()))
    
    print(colored_text(f'Enter output of question {problem} (cancel by CANCELTEST and ending by ENDTEST):', 'yellow'))
    output_sections = []
    while True:
        section = input()
        if section == ENDTEST:
            break
        if section == CANCELTEST:
            return
        output_sections.append(section)
    inputed = False
    count_of_test = int(input_sections[0])
    if len(output_sections) % count_of_test == 0:
        if input(colored_text(f'each output is {len(output_sections) // count_of_test}? (yes/no): ', 'yellow')).lower() in ['yes', 'y']:
            num_of_lines_outputs = [len(output_sections) // count_of_test] * len(num_of_lines_inputs)
            inputed = True
    if not inputed:
        num_of_lines_outputs = map(int, colored_text(input(f'Enter {output_sections[0]} number: '), 'yellow').strip().split())
    
    status = []
    for i in range(count_of_test):
        status.append((num_of_lines_inputs[i], num_of_lines_outputs[i]))
    if not modify_json(os.path.join(PARSERDIR, 'testcase.json'), problem, count_of_test, 'single', status):
        print(f'{colored_text("Error", "red")}: invalid problem name - {problem} not exist!')
        return
    
    with open(os.path.join(PARSERDIR, 'samples', problem, 'test.in'), 'w') as f:
        for section in input_sections:
            f.write(section + '\n')
    with open(os.path.join(PARSERDIR, 'samples', problem, 'test.ans'), 'w') as f:
        for section in input_sections:
            f.write(section + '\n')

# ========================================================== main

def main():
    parser = argparse.ArgumentParser(description='commands of parser information')
    parser.add_argument('-initialize', '-i' , metavar='name', type=str, help='contest name')
    parser.add_argument('-problemnum', metavar='NUM_PROBLEMS', type=int, help='Number of problems to implement')
    parser.add_argument('-problemcustom', metavar='NAME_PROBLEMS', type=str, help='name of problems to implement')
    parser.add_argument('-env', metavar='environment', type=str, help='name of problems to implement')
    parser.add_argument('-info', action='store_true', help='Show information about the competition')
    parser.add_argument('-testcase', metavar='testcase', type=str, help='about out test cases')
    parser.add_argument('-problem', '-p', metavar='problem', type=str, help='choose a problem')
    parser.add_argument('-test', '-t', metavar='test', type=str, help='choose a testcase')
    parser.add_argument('-sign', metavar='sign', type=str, help='sign of the problem')
    parser.add_argument('-language', '-lang', metavar='language', type=str, help='sign of the problem')
    args = parser.parse_args()

    if args.initialize:
        initializer(args)
    elif args.testcase:
        if args.testcase == 'status':
            testcase_status()
        elif args.testcase == 'update':
            testcase_update()
        elif args.testcase == 'refactor':
            testcase_refactor()
        elif args.testcase == 'addformat':
            testcase_addformat()
        elif args.testcase == 'opendir':
            if args.problem == None:
                print(f'{colored_text("Error", "red")}: Please provide a problem name.')
            else:
                testcase_open(args.problem.upper())
        elif args.testcase == 'flush':
            if args.problem == None:
                print(f'{colored_text("Error", "red")}: Please provide a problem name.')
            elif args.test == None:
                print(f'{colored_text("Error", "red")}: Please provide a case test (or all).')
            else:
                testcase_flush(args.problem.upper(), args.test.lower())
        elif args.testcase == 'addsingle':
            if args.problem == None:
                print(f'{colored_text("Error", "red")}: Please provide a problem name.')
            else:
                testcase_addsingle(args.problem.upper())
        else:
            print(f'{colored_text("Error", "red")}: invalid argument for testcase.')
    # elif args.info:
    #     print_competition_info()
    else:
        print("\033[91mError\033[0m: Please provide valid arguments.")

if __name__ == "__main__":
    main()
