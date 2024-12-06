from rcph.utils.imports import argparse
from rcph.utils.tools.hello import run as hello_runner
from rcph.commands.init.handler import run as init_runner
from rcph.commands.tca.handler import run as tca_runner
from rcph.commands.judge.handler import run as judge_runner
from rcph.commands.addq.handler import run as addq_runner
from rcph.commands.delq.handler import run as delq_renner
from rcph.commands.make.handler import run as make_runner
from rcph.commands.status.handler import run as status_runner
from rcph.commands.edit.handler import run as edit_runner
from rcph.commands.info.handler import run as info_runner
from rcph.commands.readme.handler import run as readme_runnder
from rcph.commands.cp.handler import run as cp_runner

from rcph.commands.asset.handler import run as asset_runner
from rcph.commands.search.handler import run as search_runner
from rcph.commands.globall.handler import run as global_runner
from rcph.commands.tcbank.handler import run as tcbank_runner
from rcph.commands.save.handler import run as save_runner
from rcph.commands.parent.handler import run as parent_runner


def create_parser():
    parser = argparse.ArgumentParser(
        description="Welcome to rcph! A CLI tool for competitive programming.",
        epilog="for more information visit: https://github.com/EnAnsari/cph",
    )
    subparsers = parser.add_subparsers(dest="command", help="Available subcommands")

    # Add the 'hello' subcommand
    hello_parser = subparsers.add_parser("hello", help="rcph hello to you!")
    hello_parser.set_defaults(func=hello_runner)

    # Add the 'init' subcommand
    init_parser = subparsers.add_parser("init", aliases=["i"], help="Initialize configuration")
    init_parser.add_argument('folder_name', help='Name of the folder to initialize.')
    init_parser.add_argument('test', nargs='?', help='is contest \'test\' or real') # if contest test it isn't save in data
    init_parser.add_argument('parent', nargs='?', help='parent portal address')
    init_parser.set_defaults(func=init_runner)

    # Add the 'tca' subcommand (test case adder)
    tca_parser = subparsers.add_parser("tca", aliases=["t"], help="test case adder")
    tca_parser.add_argument('problem', help='problem name')
    tca_parser.set_defaults(func=tca_runner)

    # Add the 'judge' subcommand
    judge_parser = subparsers.add_parser("judge", aliases=["j"], help="test case judger")
    judge_parser.add_argument('problem', nargs='?', help='problem name')
    judge_parser.set_defaults(func=judge_runner)

    # Add the 'addq' subcommand to adding questions
    addq_parser = subparsers.add_parser("addq", help="add question")
    addq_parser.add_argument('problem', help='problem name')
    addq_parser.set_defaults(func=addq_runner)

    # Add the 'delq' subcommand to deleting questions
    delq_parser = subparsers.add_parser("delq", help="delete question")
    delq_parser.add_argument('problem', help='problem name')
    delq_parser.set_defaults(func=delq_renner)

    # Add the 'make' subcommand
    make_parser = subparsers.add_parser("make", help="delete question")
    make_parser.add_argument('file', help='file name')
    make_parser.set_defaults(func=make_runner)

    # Add the 'status' subcommand for set problem status
    status_parser = subparsers.add_parser("status", help="set a status for problem")
    status_parser.add_argument('problem', help='problem name')
    status_parser.set_defaults(func=status_runner)

    # Add the 'edit' subcommand for edit contest detail
    edit_parser = subparsers.add_parser("edit", help="edit contest detail")
    edit_parser.set_defaults(func=edit_runner)

    # Add the 'info' subcommand for showing contest information
    info_parser = subparsers.add_parser("info", help="showing contest information")
    info_parser.set_defaults(func=info_runner)

    # Add the 'readme' subcommand for creating readme file
    readme_parser = subparsers.add_parser("readme", aliases=["md"], help="create readme file")
    readme_parser.add_argument('address', help='address of readme file')
    readme_parser.set_defaults(func=readme_runnder)

    # Add the 'cp' subcommand for copying files from data/template
    cp_parser =  subparsers.add_parser("cp", help="copy from template folder")
    cp_parser.add_argument('src', help='source file address')
    cp_parser.add_argument('des', nargs='?', help='destination file address')
    cp_parser.set_defaults(func=cp_runner)

    # Add the 'asset' subcommand
    asset_parser = subparsers.add_parser('asset', aliases=['ass'], help='asset file bringer')
    asset_parser.add_argument('connect', nargs='?', help='to connection an asset folder')
    asset_parser.set_defaults(func=asset_runner)

    # Add the 'save' subcommand for saving files in asset
    save_parser = subparsers.add_parser('save', help='save file in asset')
    save_parser.add_argument('file', help='file selected for save in asset/saved')
    save_parser.set_defaults(func=save_runner)

    # Add the 'parent' subcommand for parent business
    parent_parser = subparsers.add_parser('parent', help='parent business')
    parent_parser.add_argument('plus', nargs='?', help='if you want to add someone')
    parent_parser.set_defaults(func=parent_runner)

    return parser
