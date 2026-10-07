"""
list_parser.py

define ``register_list_parser``
"""

from argparse import RawDescriptionHelpFormatter

from kaye_engine.cli.blueprint.aux_output import (
    emit_str,
    fmt_ls,
    run_cmd_and_exit,
)
from kaye_engine.cli.cli_setup_guard import check_corpus_setup_for_cli
from kaye_engine.prompt.blueprint import blueprint_registry

# todo cli prompt ls additional filtering/groups

# constants  ###################################################################

_HELP = "list all registered blueprints by canonical name"


_DESCRIPTION = _HELP + """

prints each canonical name held in the blueprint registry,
sorted alphabetically, one per line"""


def _list_main(_):  ############################################################
    check_corpus_setup_for_cli()

    emit_str(fmt_ls(sorted(blueprint_registry)))


def register_list_parser(cli_subparser):  ######################################
    """
    register the ``kaye blueprint list`` subcommand parser
    """
    list_parser = cli_subparser.add_parser(
        "list",
        help=_HELP,
        description=_DESCRIPTION,
        formatter_class=RawDescriptionHelpFormatter,
        aliases=["ls"],
    )

    list_parser.set_defaults(
        func=lambda args: run_cmd_and_exit(_list_main, args)
    )
