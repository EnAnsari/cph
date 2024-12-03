from rcph.utils.imports import os
from rcph.utils.launcher import getTemplate
from rcph.utils.tools.color import colored_text

def makeTemplateFile(file_name):
    file_path = os.path.join(os.getcwd(), file_name + '.cpp')
    if os.path.exists(file_path):
        raise Exception(f'{file_name}.cpp file exist before!')
    
    template = getTemplate()
    with open(file_path, 'w') as file:
        file.write(template)

    print(colored_text(f'{file_name}.cpp file created successfully!', 'green'))