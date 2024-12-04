from .utils import *

def run(args):
    src = args.src
    des = args.des if args.des else None
    
    src_path = getSourcePath(src)
    
    copyFile(src_path, des)