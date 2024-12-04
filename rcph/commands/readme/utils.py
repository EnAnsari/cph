from rcph.utils.imports import os, pathlib
from pathlib import Path
from rcph.config.constant import *
from rcph.utils.launcher import getInfo, getSign
from rcph.utils.tools.color import colored_text

def checkExistenceDir(address):
    path = os.path.join(os.getcwd(), address)
    if not os.path.exists(path):
        raise Exception(f'path does not exist! ({path})')
    
def fileWriter(address, content):
    with open(os.path.join(os.getcwd(), address, 'README.md'), 'w') as readme_file:
        readme_file.write(content)
    print(colored_text('readme file successfully created!', 'green'))

def getRelativePath(address1, address2):
    first = Path(address1)
    second = Path(address2)
    relative_path = first.relative_to(second.resolve())
    return relative_path

def createReadme(address):
    content = ''
    info = getInfo()
    link = getRelativePath(os.getcwd(), os.path.join(os.getcwd(), address))
    print(os.path.join(os.getcwd(), address))
    print(link)


    # create first part (name / description)
    if info[DICT.NAME]:
        content += f'# 🚀 {info[DICT.NAME]} contest\n'
    if info[DICT.LINK]:
        content += f'**contest link: [{info[DICT.LINK]}]({info[DICT.LINK]})**\n'
    if info[DICT.DETAIL]:
        content += f'### overview\n{info[DICT.DETAIL]}\n'
    
    # cerate problem test case section
    if info[DICT.PROBLEMS]:
        content += f'\n## 📝 Problem Specifications\n\n'
        content += '<div align="center">\n\n'
        content += "| letter | name | status |\n"
        content += '|:---:|:---:|:---:|\n'
        for problem in info[DICT.PROBLEMS]:
            content += f'|[{problem[DICT.LETTER].upper()}]({os.path.join(".", link, problem[DICT.LETTER] + ".cpp")})|'
            content += problem[DICT.NAME] if problem[DICT.NAME] else '-empty-'
            content += f'|{problem[DICT.STATUS]}|\n'
        content += '</div>\n\n'

    content += '<br><details><summary><strong>📊 Test Cases (click to expand)</strong></summary>\n\n'
    for problem in info[DICT.PROBLEMS]:
        content += f'### problem {problem[DICT.LETTER].upper()}\n'
        tc_folder = os.path.join(os.getcwd(), RCPH_FOLDER, TESTCASE_FOLDER, problem[DICT.LETTER])
        counter = 1
        while True:
            input_path = os.path.join(tc_folder, str(counter) + '.in')
            output_path = os.path.join(tc_folder, str(counter) + '.ans')
            if not os.path.exists(input_path) or not os.path.exists(output_path):
                break
            with open(input_path, 'r') as fin, open(output_path, 'r') as fout:
                content += f'#### Example {counter}:\n'
                content += f'* **input:**\n'
                content += f'```bash\n{fin.read()}\n```\n'
                content += f'* **output:**\n'
                content += f'```bash\n{fout.read()}\n```\n\n'
            counter += 1
        if counter == 1: # test case was empty!
            content += f'\nproblem {problem[DICT.LETTER].upper()} has not any test case!\n'
    content += '\n</details>'

    # create about me section and about rcph
    content += '\n\n### ⚡ About Me\n'
    sign = getSign()
    for line in sign:
        content += f'* **{line.strip()}**\n'

    content += '\n💡 ***see more about rcph in [our repository +](https://github.com/EnAnsari/cph)***\n'

    return content + '\n'