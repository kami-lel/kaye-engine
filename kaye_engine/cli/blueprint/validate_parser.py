"""
validate_parser.py

define ``register_validate_parser``
"""

from argparse import RawDescriptionHelpFormatter

import kamilog
from kaye_engine import LOGGER_NAME
from kaye_engine.cli.blueprint.aux_input import get_cmd_blueprint
from kaye_engine.cli.blueprint.aux_output import run_cmd_and_exit
from kaye_engine.cli.blueprint.blueprint_arg_parser import (
    build_blueprint_arg_parser,
)
from kaye_engine.cli.cli_setup_guard import check_corpus_setup_for_cli
from kaye_engine.prompt.blueprint import validate_blueprint
from kamilog import (
    add_verbose_arguments,
    set_logging_level_by_namespace,
)

# logger  ######################################################################
logger = kamilog.getLogger(LOGGER_NAME)

# constants  ###################################################################
_HELP = "check a blueprint is sound: exit 0 if so, 1 with the reason if not"

_DESCRIPTION = _HELP + """

a blueprint is sound when every dependency name is registered and, while a
corpus is loaded, every node path exists in it; nothing is printed on success

select BLUEPRINT by canonical name in blueprint registry:

    kaye-engine blueprint validate my-blueprint

reading blueprint from stdin, a preview tree or JSON:

    kaye-engine blueprint validate < my-blueprint.json
    cat my-tree.txt | kaye-engine blueprint validate
"""


# auxiliaries  #################################################################
def _validate_main(args):
    set_logging_level_by_namespace(args, logger=logger)
    check_corpus_setup_for_cli()

    validate_blueprint(get_cmd_blueprint(args.BLUEPRINT).blueprint)


# Public API  ##################################################################
def register_validate_parser(cli_subparser):
    """
    register the ``kaye blueprint validate`` subcommand parser
    """
    validate_parser = cli_subparser.add_parser(
        "validate",
        help=_HELP,
        description=_DESCRIPTION,
        formatter_class=RawDescriptionHelpFormatter,
        aliases=["v"],
        parents=[build_blueprint_arg_parser()],
    )

    add_verbose_arguments(validate_parser)

    validate_parser.set_defaults(
        func=lambda args: run_cmd_and_exit(_validate_main, args)
    )
