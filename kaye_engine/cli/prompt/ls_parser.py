"""
ls_parser.py

define ``register_ls_subparser``
"""

from kaye_engine.prompt.blueprint import BLUEPRINT_REGISTRIES

# todo cli prompt ls additional filtering/groups

# constants  ###################################################################

_HELP = "list names of all registered blueprints"


_DESCRIPTION = _HELP + """

prints the name of each registered blueprint in BLUEPRINT_REGISTRIES,
sorted alphabetically, one per line"""


def _ls_main(_):  ##############################################################
    for name in sorted(BLUEPRINT_REGISTRIES):
        print(name)


def register_ls_subparser(cli_subparser):  #####################################
    """
    register the ``kaye prompt ls`` subcommand parser
    """
    ls_parser = cli_subparser.add_parser(
        "ls", help=_HELP, description=_DESCRIPTION
    )

    ls_parser.set_defaults(func=_ls_main)
