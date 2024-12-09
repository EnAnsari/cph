from rcph.utils.imports import os, shutil
from rcph.config.data import DATA_ADDRESS
from rcph.config.constant import *
from rcph.utils.tools.color import colored_text

def getSourcePath(address):
    src_path = os.path.join(DATA_ADDRESS, DATA.TEMPLATE_FOLDER, *address.split('/'))
    if not os.path.isfile(src_path):
        raise Exception(f'thre is not any file by path: {src_path}')

    return src_path

def copyFile(src, des):
    if des == None:
        des = os.path.basename(src)
    
    des_path = os.path.join(os.getcwd(), *des.split('/')[:-1])
    os.makedirs(des_path, exist_ok=True)

    des_path = os.path.join(des_path, des.split('/')[-1])
    shutil.copy(src, des_path)

def walkInTemplate(directory = os.path.join(DATA_ADDRESS, DATA.TEMPLATE_FOLDER), prefix=""):
    print(colored_text(f"{prefix}{os.path.basename(directory)}/", 'yellow'))
    prefix += "    "
    for item in os.listdir(directory):
        item_path = os.path.join(directory, item)
        if os.path.isdir(item_path):
            walkInTemplate(item_path, prefix)
        else:
            print(colored_text(f"{prefix}{item}", 'cyan'))
