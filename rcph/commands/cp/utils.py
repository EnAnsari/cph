from rcph.utils.imports import os, shutil
from rcph.config.data import DATA_ADDRESS
from rcph.config.constant import *

def getSourcePath(address):
    src_path = os.path.join(DATA_ADDRESS, TEMPLATE_FOLDER, *address.split('/'))
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