# just run it first time you use this program (before pip install .)

import os

with open(os.path.join('rcph', 'config', 'data.py'), 'w') as file:
    file.write(f"DATA_ADDRESS = \'{os.path.join(os.getcwd(), 'data')}\'")