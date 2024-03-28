import os
import argparse
import json
import random
import datetime

MAXSIGNLINE = 20

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
    json_address = os.path.join(parser_address, 'info.json')
    script_content = f'''#!/bin/bash\n\nfile_address=$(jq -r '.file_executable' {json_address})\n\npython3 "$file_address" "$@"'''
    script_address = os.path.join(parser_address, 'r')
    with open(script_address, 'w') as f:
        f.write(script_content)
    os.chmod(script_address, 0o755)  # Add execute permissions to the script


def initializer(args):
    type, name = args.initialize
    folder_names = []
    if type == 'contest' or type == 'c':
        if args.problemnum:
            folder_names = [chr(ord('A') + i) for i in range(args.problemnum)]
        elif args.problemcustom:
            folder_names = args.problemcustom.split()
        else:
            print(f'{colored_text("error", "red")}: Enter num of qustion by [-problemnum] or [-problemcustom]')
            return

    elif type == 'question' or type == 'q':
        folder_names.append(name)
    else:
        print(f'{colored_text("error", "red")}: invalid type - must be [contest] or [question]')
        return

    with open(os.path.join(os.path.dirname(__file__), 'main.cpp'), 'r') as templatefile:
        template_content = templatefile.read()

    with open(os.path.join(os.path.dirname(__file__), 'sign.txt'), 'r') as sign_file:
        sign_content = sign_file.readlines()

    with open(os.path.join(os.path.dirname(__file__), 'quotes.txt'), 'r') as quotes_file:
        quotes = quotes_file.readlines()

    contest_dir = os.path.join(os.getcwd(), name)
    if(os.path.exists(contest_dir)):
        print(f"{colored_text('Error', 'red')}: '{name}' already exists.")
        return
    os.makedirs(contest_dir, exist_ok=True)


    for problem_name in folder_names:
        if type == 'question' or type == 'q':
            problem_dir = contest_dir
        else:
            problem_dir = os.path.join(contest_dir, problem_name)
            os.makedirs(problem_dir, exist_ok=True)
        
        with open(os.path.join(problem_dir, 'main.cpp'), 'w') as f:
            f.write('/*\n')
            if type != 'question' and type != 'q':
                f.write(f'\tcontest name: {name}\n')
            f.write(f'\tproblem name: {problem_name}\n')
            f.write(f'\tTime: {datetime.datetime.now().strftime("%Y-%m-%d %H:%M")}\n')
            for sign_line in sign_content:
                f.write(f'\t{sign_line}')
            f.write(f'\n\n{make_a_quote(quotes)}\n*/\n\n')
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
            "type": type,
            "name": name,
            "num_problems": len(folder_names),
            "samples_state": "empty",
            "file_executable": __file__,
        }
        with open(os.path.join(parser_dir, 'info.json'), 'w') as info_file:
            json.dump(info, info_file, indent=4)


# ========================================================== tester

def main():
    parser = argparse.ArgumentParser(description='commands of parser information')
    parser.add_argument('-initialize',  nargs=2, metavar=('type', 'name'), type=str, help='Name and type(contest or question)')
    parser.add_argument('-problemnum', metavar='NUM_PROBLEMS', type=int, help='Number of problems to implement')
    parser.add_argument('-problemcustom', metavar='NAME_PROBLEMS', type=str, help='name of problems to implement')
    parser.add_argument('-env', metavar='environment', type=str, help='name of problems to implement')
    parser.add_argument('-info', action='store_true', help='Show information about the competition')
    args = parser.parse_args()

    if args.initialize:
        initializer(args)
    # elif args.info:
    #     print_competition_info()
    else:
        print("\033[91mError\033[0m: Please provide valid arguments.")

if __name__ == "__main__":
    main()
