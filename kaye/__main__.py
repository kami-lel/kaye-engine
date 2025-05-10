"""
define the CLI for ``kaye``
"""

# fixme better __doc__

# TODO TODO

import argparse

from kaye.gen_prompt.prompt_blueprint_loader import (
    get_embedded_prompt_blueprints_names,
)


# setup main parser
def _kaye_main(_):
    """
    main behvaior when calling ``python -m kaye``
    """
    kaye_psr.print_help()


kaye_psr = argparse.ArgumentParser(prog="kaye", description=__doc__)
kaye_psr.set_defaults(func=_kaye_main)

kaye_subpsr = kaye_psr.add_subparsers(title="subcommands")


# setup subparser: kaye prompt
def _prompt_main(_):
    """
    main behvaior when calling ``python -m kaye prompt``
    """
    prompt_psr.print_help()


PROMPT_HELP_TEXT = "prompt related"  # TODO
prompt_psr = kaye_subpsr.add_parser(
    "prompt", help=PROMPT_HELP_TEXT, description=PROMPT_HELP_TEXT
)
prompt_psr.set_defaults(func=_prompt_main)

prompt_subpsr = prompt_psr.add_subparsers(title="subcommands")


# setup subparser: kaye prompt ls
def _ls_main(_):
    """
    main behvaior when calling ``python -m kaye prompt ls``
    """
    print("all available embedded blueprints:")
    for blueprint_name in get_embedded_prompt_blueprints_names():
        print("\t{}".format(blueprint_name))


LS_HELP_TEXT = "show all available embedded blueprints"
ls_psr = prompt_subpsr.add_parser(
    "ls",
    help=LS_HELP_TEXT,
    description=LS_HELP_TEXT,
)
ls_psr.set_defaults(func=_ls_main)


# setup subparser: kaye prompt
# TODO TODO


if __name__ == "__main__":
    args = kaye_psr.parse_args()
    args.func(args)
