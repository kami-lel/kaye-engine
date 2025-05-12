"""
CLI for Python module ``kaye``
"""

from argparse import ArgumentParser, FileType

from kaye.gen_prompt.prompt_blueprint_loader import (
    get_embedded_prompt_blueprints_names,
    load_embedded_prompt_blueprint,
)

# get all available blueprints at runtime
blueprint_names = sorted(get_embedded_prompt_blueprints_names())


# setup main parser
def _kaye_main(_):
    # when calling ``python -m kaye``
    kaye_psr.print_help()


kaye_psr = ArgumentParser(prog="kaye", description=__doc__)
kaye_psr.set_defaults(func=_kaye_main)
kaye_subpsr = kaye_psr.add_subparsers(title="subcommands")


# setup subparser: kaye prompt
def _prompt_main(_):
    # when calling ``python -m kaye prompt``
    prompt_psr.print_help()


PROMPT_HELP_TEXT = (
    "dynamically generate AI system prompt with a prompt blueprint"
    " as a subset of the prompt corpus"
)
prompt_psr = kaye_subpsr.add_parser(
    "prompt",
    help=PROMPT_HELP_TEXT,
    description=PROMPT_HELP_TEXT,
)

prompt_psr.set_defaults(func=_prompt_main)
prompt_subpsr = prompt_psr.add_subparsers(
    description="utility functions related to prompt generation"
)


# setup subparser: kaye prompt ls
def _prompt_ls_main(_):
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
ls_psr.set_defaults(func=_prompt_ls_main)


# args shared by gen and show
arg_sharing_psr = ArgumentParser(add_help=False)

# positional argument
arg_sharing_psr.add_argument(
    "BLUEPRINT",
    help="name of any embedded blueprints",
    type=str,
)
# options
arg_sharing_psr.add_argument(
    "-f",
    "--file",
    metavar="FILE",
    type=FileType(mode="w"),
    nargs="?",
    help="save the result to file",
)


# setup subparser: kaye prompt gen
def _prompt_gen_main(args):
    # when calling ``python -m kaye prompt gen``
    bluerpint_name = args.BLUEPRINT
    blueprint_obj = load_embedded_prompt_blueprint(bluerpint_name)
    prompt_content = str(blueprint_obj)

    # with --file FILE
    if args.file:
        with args.file as f:
            f.write(prompt_content)
    else:
        print(prompt_content)

    # todo allow user set preview line, etc.

    # TODO interactive mode
    # TODO source file


GEN_HELP_TEXT = "generate concreate prompt from blueprint"
gen_psr = prompt_subpsr.add_parser(
    "gen",
    help=GEN_HELP_TEXT,
    description=GEN_HELP_TEXT,
    parents=[
        arg_sharing_psr,
    ],
)
gen_psr.set_defaults(func=_prompt_gen_main)


# setup subparser: kaye prompt show
def _prompt_show_main(args):
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


SHOW_HELP_TEXT = "show content of any of embedded blueprints"
show_psr = prompt_subpsr.add_parser(
    "show",
    help=SHOW_HELP_TEXT,
    description=SHOW_HELP_TEXT,
    parents=[
        arg_sharing_psr,
    ],
)
show_psr.set_defaults(func=_prompt_show_main)


if __name__ == "__main__":
    parsed_args = kaye_psr.parse_args()
    parsed_args.func(parsed_args)  # call respective main function
