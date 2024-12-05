from .utils import *

def run(args):
    file = args.file
    file_path = checkExistence(file)
    saved_path = explore()
    fileSaving(file_path, saved_path)