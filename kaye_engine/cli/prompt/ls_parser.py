"""
ls_parser.py

define ``register_ls_parser``
"""

from kaye_engine.cli.cli_setup_guard import check_corpus_setup_for_cli
from kaye_engine.prompt.blueprint import blueprint_registry

# todo cli prompt ls additional filtering/groups

# constants  ###################################################################

_HELP = "list names of all registered blueprints"


_DESCRIPTION = _HELP + """

prints the name of each registered blueprint in blueprint_registry,
sorted alphabetically, one per line"""


def _ls_main(_):  ##############################################################
    check_corpus_setup_for_cli()

    for name in sorted(blueprint_registry):
        print(name)


def register_ls_parser(cli_subparser):  ########################################
    """
    register the ``kaye prompt ls`` subcommand parser
    """
    ls_parser = cli_subparser.add_parser(
        "ls", help=_HELP, description=_DESCRIPTION
    )

    ls_parser.set_defaults(func=_ls_main)
