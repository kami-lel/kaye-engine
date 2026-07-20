"""
ls_parser.py

define ``register_ls_subparser``
"""

from kaye import logger

# constants  ###################################################################

_HELP = "list names of all available embedded blueprints"


def _ls_main(_):  ##############################################################
    # TODO: list names of all available embedded blueprints
    logger.error("kaye prompt ls: not implemented yet")
    raise NotImplementedError


def register_ls_subparser(cli_subparser):  #####################################
    """
    register the ``kaye prompt ls`` subcommand parser
    """
    ls_parser = cli_subparser.add_parser("ls", help=_HELP, description=_HELP)

    ls_parser.set_defaults(func=_ls_main)
