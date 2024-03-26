import os
import argparse
import json


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


def initialize_contest(contest_name, num_problems):
    # Create contest directory
    contest_dir = os.path.join(os.getcwd(), contest_name)
    if(os.path.exists(contest_dir)):
        print(f"\033[91mContest '{contest_name}' already exists.\033[0m")
        return
    os.makedirs(contest_dir, exist_ok=True)

    with open(os.path.join(os.path.dirname(__file__), 'main.cpp'), 'r') as parser_file:
        parser_content = parser_file.read()

    parser_dir = os.path.join(contest_dir, '.parser')
    os.makedirs(parser_dir, exist_ok=True)
    
    # Create samples directory
    samples_dir = os.path.join(parser_dir, 'samples')
    os.makedirs(samples_dir, exist_ok=True)
    for i in range(num_problems):
        problem_name = chr(ord('A') + i)
        problem_dir = os.path.join(samples_dir, problem_name)
        os.makedirs(problem_dir, exist_ok=True)

    # Create problem directories
    for i in range(num_problems):
        problem_name = chr(ord('A') + i)
        problem_dir = os.path.join(contest_dir, problem_name)
        os.makedirs(problem_dir, exist_ok=True)
        
        # Write contest name and problem name to main.cpp
        with open(os.path.join(problem_dir, 'main.cpp'), 'w') as f:
            f.write(f'// {contest_name}: {problem_name}\n\n')
            f.write(parser_content)

    # Create info.json file
    info = {
        "contest_name": contest_name,
        "num_problems": num_problems,
        "samples_state": "empty"
    }
    with open(os.path.join(parser_dir, 'info.json'), 'w') as info_file:
        json.dump(info, info_file, indent=4)


def print_competition_info():
    parser_dir = os.path.join(os.getcwd(), '.parser')
    info_file_path = os.path.join(parser_dir, 'info.json')

    if os.path.exists(info_file_path):
        with open(info_file_path, 'r') as info_file:
            info = json.load(info_file)
            print("Competition Name:", colored_text(info.get("contest_name"), "green"))
            print("Number of Problems:", colored_text(info.get("num_problems"), "green"))
            samples_status = info.get("samples_state")
            if samples_status == "empty":
                samples_status = colored_text(info.get("samples_state"), "red")
            print("Samples State:", samples_status)
    else:
        print(f"{colored_text('Error', 'red')}: You are not in a competition directory or info file is missing.")


def main():
    parser = argparse.ArgumentParser(description='commands of parser information')
    parser.add_argument('-initialize', metavar='contest_name', type=str, help='Name of the coding competition round')
    parser.add_argument('-problems', metavar='NUM_PROBLEMS', type=int, help='Number of problems to implement')
    parser.add_argument('-info', action='store_true', help='Show information about the competition')
    args = parser.parse_args()

    if args.initialize and args.problems:
        initialize_contest(args.initialize, args.problems)
    elif args.info:
        print_competition_info()
    else:
        print("\033[91mError\033[0m: Please provide valid arguments.")

if __name__ == "__main__":
    main()
