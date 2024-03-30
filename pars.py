import os
import argparse
import json
import random
import datetime
import subprocess
import timeit
import resource

MAXSIGNLINE = 20
ENDTEST = 'ENDTEST'
CANCELTEST = 'CANCELTEST'
FILEDIR = os.path.dirname(__file__)
PARSERDIR = os.path.join(os.getcwd(), '.parser')

def colored_text(text, color,  *args, reset = True):

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

    result = f'\033{1 if light else 0};{colors.get(color.lower(), '')}m'
    for arg in args:
        if arg.lower in colors.keys():
            result += f'{colors[arg.lower()]}m'

    return colors.get(color.upper(), '') + colors.get('UNDERLINE', '') + str(text) + '0' if reset else ''

print(colored_text('hello', 'light blue', 'underline', reset=False))
print('hello world')

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

def create_info_file(parser_address, name, signflag, lang, folder_names):
    problem_count = len(folder_names)
    problems = {}
    for folder_name in folder_names:
        problems[folder_name] = {
            "name": '',
            "status": "raw",
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
        create_info_file(parser_dir, name, signflag, lang, folder_names)
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

def testcase_reformat():
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

# ========================================================== judge

def compile_code(code_path):
    process = subprocess.run(['g++', code_path, '-o', 'main'], capture_output=True, text=True)  # Compile
    if process.returncode != 0:
        return {'status': 'Incorrect (Compilation error)', 'output': process.stderr, 'error': None, 'execution_time': None, 'memory_usage': None}
    return {'status': 'success', 'output': None, 'error': None, 'execution_time': None, 'memory_usage': None}

def judge_code(code_path, input_file, output_file, compile = True):
    try:
        with open(output_file, 'r') as f:
            expected_output = f.read().strip()

        input_data = open(input_file, 'rb').read().decode('utf-8')
        start_memory = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
        start_time = timeit.default_timer()

        if code_path.endswith('.py'):
            process = subprocess.run(['python', code_path], input=input_data, capture_output=True, text=True)
        else:
            if compile:
                compile_result = compile_code(code_path)
                if compile_result['status'] != 'success':
                    return compile_result
            process = subprocess.run(['./main'], input=input_data, capture_output=True, text=True)
        end_time = timeit.default_timer()

        execution_time = end_time - start_time
        actual_output = process.stdout.strip()

        end_memory = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
        memory_usage = end_memory - start_memory

        if actual_output == expected_output:
            return {'status': 'Correct', 'output': actual_output, 'error': None, 'execution_time': execution_time, 'memory_usage': memory_usage}
        else:
            return {'status': 'Incorrect', 'output': actual_output, 'error': None, 'execution_time': execution_time, 'memory_usage': memory_usage}

    except Exception as e:
        return {'status': 'Error', 'output': None, 'error': str(e), 'execution_time': None, 'memory_usage': None}


# def judge(args):
#     problem = args.problem.upper()
#     jsonfile = os.path.join(PARSERDIR, 'info.json')
#     with open(jsonfile, 'r') as infile:
#         info = json.load(infile)
#     jsonfile = os.path.join(PARSERDIR, 'testcase.json')
#     with open(jsonfile, 'r') as infile:
#         testcase = json.load(infile)
#     if problem not in info['folder_names']:
#         print(f'{colored_text("Error", "red")}: invalid problem name - {problem} not exist!')
#         return

#     # if args.just:
#     #     if args.just == 'compile' and info['problems'][problem]['lang'] == 'cpp':
#     #         result = compile_code(os.path.join(PARSERDIR, problem, 'main.cpp'))
#     #         print(result)
#     #         return
#     #     elif args.just == 'run':
#     #         result = judge_code(os.path.join(PARSERDIR, problem, 'main.cpp'), os.path.join(PARSERDIR, 'samples', problem, 'test.in'), os.path.join(PARSERDIR, 'samples', problem, 'test.ans', False))
#     #         print(result)
#     #         return
#     #     else :
#     #         print(f'{colored_text("Error", "red")}: invalid argument for just. [only compile (for cpp) | run]')
#     #         return
    
#     # if args.test.lower() == 'off':
#     #     pass
    

#     if testcase['problems'][problem]['type'] == 'empty':
#         print(f'{colored_text("Error", "red")}: test case not found')
#         return
#     if testcase['problems'][problem]['type'] == 'single':
#         input = os.path.join(PARSERDIR, 'samples', problem, 'test.in')
#         output = os.path.join(PARSERDIR, 'samples', problem, 'test.ans')
#         file = os.path.join(os.getcwd(), problem, f'main.{info['problems'][problem]['lang']}')
#         result = judge_code(file, input, output)
#         description = []
#         status = result["status"] == "Correct"
#         if args.timing and result["execution_time"] > info['problems'][problem]['time_exceed']:
#             status = False
#             description.append('time exceeded')
#         if args.memory and result['memory_usage'] > info['problems'][problem]['memory_exceed']:
#             status = False
#             description.append('memory exceeded')
 
#         my_output = result['output']
#         with open(output, 'r') as output:
#             original_output = output.read()
#         with open(input, 'r') as input:
#             original_input = input.read()

#         i = 1
#         inpult_cur_line = 1
#         output_cur_line = 1
#         for inputline, outputline in testcase['problems'][problem]['status'].split():
#             pass
 
#         print(f'Status: {colored_text("Accept", "green") if status else colored_text("Reject", "red")}')
#         if not status:
#             print(colored_text)
#             for line in description:
#                 print(line)
#         print(f'Execution Time: {colored_text((result["execution_time"]), "green" if "time exceeded" not in description else "red")}')
#         print(f'Memory usage: {colored_text((result["memory_usage"]), "green" if "memory exceeded" not in description else "red")} bytes')

#         return
    

# ========================================================== main

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
    -status [done | accept | running | raw | out]: new status to choose
    -timing: new time to choose
    -memory: new memory to choose
    -sign [on | off]: sign of the problem
    -contest: adding descrition and link of the contest

    -ending: ending the competition
        markdown: create a markdown file of the contest
        removeraw: remove the raw status of the problem to out status
        removemain: remove the main file of the problems
        removeetc: remove the etc files of the problems except the main code
    
    
    -assets: create a assets code for the contest
        [line to add | file to add(by line or without)] [address of asset | main.cpp (template)]
        -byetc: adding header and main func too

"""

def main():
    parser = argparse.ArgumentParser(description='commands of parser information')
    parser.add_argument('-initialize', '-i' , metavar='name', type=str, help='contest name')
    parser.add_argument('-problemnum', metavar='NUM_PROBLEMS', type=int, help='Number of problems to implement')
    parser.add_argument('-problemcustom', metavar='NAME_PROBLEMS', type=str, help='name of problems to implement')
    parser.add_argument('-env', metavar='environment', type=str, help='name of problems to implement')
    parser.add_argument('-info', '-i', action='store_true', help='Show information about the competition')
    parser.add_argument('-testcase', metavar='testcase', type=str, help='about out test cases')
    parser.add_argument('-problem', '-p', metavar='problem', type=str, help='choose a problem')
    parser.add_argument('-test', '-t', metavar='test', type=str, help='choose a testcase')
    parser.add_argument('-sign', metavar='sign', type=str, help='sign of the problem')
    parser.add_argument('-language', '-lang', metavar='language', type=str, help='sign of the problem')
    parser.add_argument('-judge', '-j', metavar='judge', type=str, help='sign of the problem')
    parser.add_argument('-just', metavar='just', type=str, help='just something [compile | run]')
    parser.add_argument('-timing', action='timing', help='by time or not')
    parser.add_argument('-memory', action='memory', help='by memory used or not')
    args = parser.parse_args()

    if args.initialize:
        initializer(args)
    elif args.judge:
        judge(args)
    elif args.testcase:
        if args.testcase == 'status':
            testcase_status()
        elif args.testcase == 'update':
            testcase_update()
        elif args.testcase == 'reformat':
            testcase_reformat()
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
        # "pri":("9mError0: Please provide valid arguments."),
        pass

# if __name__ == "__main__":
    # main()