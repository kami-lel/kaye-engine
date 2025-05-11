"""
CLI for Python module ``kaye``
"""

import argparse

from kaye.gen_prompt.prompt_blueprint_loader import (
    get_embedded_prompt_blueprints_names,
    load_embedded_prompt_blueprint,
)

# get all available blueprints at runtime
blueprint_names = get_embedded_prompt_blueprints_names()


# setup main parser
def _kaye_main(_):
    # when calling ``python -m kaye``
    kaye_psr.print_help()


kaye_psr = argparse.ArgumentParser(prog="kaye", description=__doc__)
kaye_psr.set_defaults(func=_kaye_main)

kaye_subpsr = kaye_psr.add_subparsers(title="subcommands")


# setup subparser: kaye prompt
def _prompt_main(_):
    # when calling ``python -m kaye prompt``
    prompt_psr.print_help()


PROMPT_HELP_TEXT = "prompt related"  # TODO
prompt_psr = kaye_subpsr.add_parser(
    "prompt", help=PROMPT_HELP_TEXT, description=PROMPT_HELP_TEXT
)
prompt_psr.set_defaults(func=_prompt_main)

prompt_subpsr = prompt_psr.add_subparsers(title="subcommands")

# TODO allow render


# setup subparser: kaye prompt ls
def _ls_main(_):
    # when calling ``python -m kaye prompt ls``
    print("all available embedded blueprints:\n")
    for blueprint_name in blueprint_names:
        print(blueprint_name)


LS_HELP_TEXT = "show all available embedded blueprints"
ls_psr = prompt_subpsr.add_parser(
    "ls",
    help=LS_HELP_TEXT,
    description=LS_HELP_TEXT,
)
ls_psr.set_defaults(func=_ls_main)


# setup subparser: kaye prompt show
SHOW_HELP_TEXT = "show content of any of embedded blueprints"
show_psr = prompt_subpsr.add_parser(
    "show", help=SHOW_HELP_TEXT, description=SHOW_HELP_TEXT
)

# positional argument with choices
show_psr.add_argument(
    "BLUEPRINT",
    help="name of any embedded blueprints",
    choices=blueprint_names,
    type=str,
)

# options
show_psr.add_argument(
    "-f",
    "--file",
    metavar="FILE",
    type=argparse.FileType(mode="w"),
    nargs=None,
    help="save the prompt blueprint to the specified file",
)


def _show_main(args):
    # when calling ``python -m kaye prompt show``
    bluerpint_name = args.BLUEPRINT
    blueprint_obj = load_embedded_prompt_blueprint(bluerpint_name)
    blueprint_content = repr(blueprint_obj)
    # todo allow user set preview line, etc.

    # with --file FILE
    if args.file:
        with args.file as f:
            f.write(blueprint_content)
    else:
        print(blueprint_content)


show_psr.set_defaults(func=_show_main)


if __name__ == "__main__":
    parsed_args = kaye_psr.parse_args()
    parsed_args.func(parsed_args)  # call respective main function
