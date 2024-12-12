from rcph.utils.imports import argparse
from rcph.utils.tools.hello import run as hello_runner
from rcph.commands.init.handler import run as init_runner
from rcph.commands.info.handler import run as info_runner
from rcph.commands.resign.handler import run as resign_runner
from rcph.commands.cf.handler import run as cf_runner
from rcph.commands.tca.handler import run as tca_runner
from rcph.commands.judge.handler import run as judge_runner
from rcph.commands.make.handler import run as make_runner
from rcph.commands.cp.handler import run as cp_runner
from rcph.commands.readme.handler import run as readme_runnder
from rcph.commands.question.handler import run as question_runner
from rcph.commands.asset.handler import run as asset_runner
from rcph.commands.search.handler import run as search_runner
from rcph.commands.globall.handler import run as global_runner
from rcph.commands.connect.handler import run as connect_runner

# Create the argument parser
def create_parser():
    parser = argparse.ArgumentParser(
        description="Welcome to rcph! A CLI tool for competitive programming.",
        epilog="For more information, visit: https://github.com/EnAnsari/cph",
    )
    subparsers = parser.add_subparsers(dest="command", help="Available subcommands")

    # Define subcommands
    def add_subcommand(name, runner, help_text, aliases=None, arguments=None):
        subcommand_parser = subparsers.add_parser(name, help=help_text, aliases=aliases or [])
        if arguments:
            for arg in arguments:
                subcommand_parser.add_argument(*arg["args"], **arg["kwargs"])
        subcommand_parser.set_defaults(func=runner)


    add_subcommand("hello", hello_runner, "rcph says hello to you!")
    add_subcommand("codeforces", cf_runner, "codeforces contest parser",  aliases=["cf"])
    add_subcommand("init", init_runner, "Initialize configuration", aliases=["i"],
        arguments=[
            {"args": ["folder_name"], "kwargs": {"help": "Name of the folder to initialize."}},
            {"args": ["parent"], "kwargs": {"nargs": "?", "help": "Parent portal address"}},
            {"args": ["test"], "kwargs": {"nargs": "?", "help": "Is contest 'test' or real?"}},
        ],
    )
    add_subcommand("info", info_runner, "Display contest information",
        arguments=[
            {"args": ["subcommand1"], "kwargs": {"nargs": "?", "help": "can be (edit|status|parent|db)"}},
            {"args": ["subcommand2"], "kwargs": {"nargs": "?", "help": "for status: <problem> and for parent <+> or <choose> or -empty- and for db <add> <rm> -empty-"}}
        ],
    )
    add_subcommand('resign', resign_runner, 'resigning problems', aliases=["sign"],
        arguments=[{"args": ['problem'], "kwargs": {"help": "problem to resign"}}]
    )
    add_subcommand("tca", tca_runner, "Test case adder", aliases=["t"],
        arguments=[{"args": ["problem"], "kwargs": {"help": "Problem name"}}],
    )
    add_subcommand("judge", judge_runner, "Test case judger", aliases=["j"],
        arguments=[{"args": ["problem"], "kwargs": {"nargs": "?", "help": "Problem name"}}],
    )
    add_subcommand("make", make_runner, "Create a template", arguments=[{"args": ["file"], "kwargs": {"help": "File name"}}])
    add_subcommand("cp", cp_runner, "Copy from the template folder",
        arguments=[
            {"args": ["src"], "kwargs": {"nargs": "?", "help": "Source file address"}},
            {"args": ["des"], "kwargs": {"nargs": "?", "help": "Destination file address"}},
        ],
    )
    add_subcommand("readme", readme_runnder, "Create a readme file", aliases=["md"],
        arguments=[{"args": ["address"], "kwargs": {"help": "Address of the readme file"}}],
    )
    add_subcommand("question", question_runner, "add and remove problems", aliases=['q'],
        arguments=[
            {"args": ["operation"], "kwargs": {"help": "operation add or remove"}},
            {"args": ["problem"], "kwargs": {"help": "problem letter"}},
        ],
    )
    add_subcommand("asset", asset_runner, "Asset file bringer", aliases=["ass"],
        arguments=[
            {"args": ["subcommand"], "kwargs": {"nargs": "?", "help": "Saving a file"}},
            {"args": ["file"], "kwargs": {"nargs": "?", "help": "file to save"}}
        ],
    )
    add_subcommand("global", global_runner, "Explore contests")
    add_subcommand("search", search_runner, "Search functionality")
    add_subcommand('connect', connect_runner, 'connecting tcbank, asset, chromedriver',
        arguments=[{'args': ['file'], 'kwargs': {'nargs': '?', 'help': 'if we want to choose a file'}}]
    )
    return parser
