from .utils import *

def run(args):
    address = args.address
    checkExistenceDir(address)

    readme_content = createReadme(address)
    fileWriter(address, readme_content)