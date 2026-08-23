"""
dynamic_substitution_parser.py

define ``register_dynamic_substitution_parser``
"""

from argparse import RawDescriptionHelpFormatter

from kaye_engine import LOGGER_NAME, kamilog
from kaye_engine.kamilog import (
    add_verbose_arguments,
    set_logging_level_by_namespace,
)
from kaye_engine.prompt.blueprint.dynamic_substitution import (
    dynamic_substitution_registry,
)

# logger  ######################################################################
logger = kamilog.getLogger(LOGGER_NAME)

# constants  ###################################################################
_HELP = "print a dynamic substitution's content, or list all of them"

_DESCRIPTION = _HELP + """

prints the content of the dynamic substitution registered under NAME:

    kaye-engine dynamic-substitution my-canonical-name

list every registered dynamic substitution, sorted alphabetically:

    kaye-engine dynamic-substitution ls
"""


# auxiliaries  #################################################################
def _dynamic_substitution_main(args):
    set_logging_level_by_namespace(args, logger=logger)

    if args.NAME == "ls":
        for name in sorted(dynamic_substitution_registry):
            print(name)
        return

    try:
        substitution = dynamic_substitution_registry[args.NAME]
    except KeyError as err:
        logger.critical("unknown dynamic substitution:\t" + args.NAME)
        raise SystemExit(1) from err

    print(substitution.generate())


# Public API  ##################################################################
def register_dynamic_substitution_parser(cli_subparser):
    """
    register the ``kaye-engine dynamic-substitution`` subcommand parser
    """
    dynamic_substitution_parser = cli_subparser.add_parser(
        "dynamic-substitution",
        help=_HELP,
        description=_DESCRIPTION,
        formatter_class=RawDescriptionHelpFormatter,
        aliases=["ds"],
    )

    # add arguments  -------------------------------------------------------
    dynamic_substitution_parser.add_argument(
        "NAME",
        help="dynamic substitution canonical name; NAME=ls: list all",
    )
    add_verbose_arguments(dynamic_substitution_parser)

    dynamic_substitution_parser.set_defaults(func=_dynamic_substitution_main)
