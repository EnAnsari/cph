from .utils import getSourcePath, copyFile, walkInTemplate

def run(args):
    if not args.src:
        walkInTemplate()
    else:
        src_path = getSourcePath(args.src)
        copyFile(src_path, args.des)