"""
dynamic_substitution_parser.py

define ``register_dynamic_substitution_parser``
"""

from argparse import RawDescriptionHelpFormatter

import kamilog
from kaye_engine.cli.list_view import (
    NAME_LIST_DESTS,
    add_name_list_flags,
    print_names,
    reject_given_flags,
    track_given_flags,
)
from kaye_engine.cli.verbosity import apply_verbosity_arg
from kaye_engine import LOGGER_NAME
from kamilog import (
    add_verbose_arguments,
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

list every registered dynamic substitution, sorted alphabetically
(default when NAME is omitted):

    kaye-engine dynamic-substitution ls
    kaye-engine dynamic-substitution
"""


# auxiliaries  #################################################################
def _dynamic_substitution_main(args):
    apply_verbosity_arg(args)

    if args.NAME == "ls":
        print_names(
            args,
            "dynamic substitutions",
            sorted(dynamic_substitution_registry),
        )
        return

    reject_given_flags(args, NAME_LIST_DESTS, "entry mode")

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
        nargs="?",
        default="ls",
        help="dynamic substitution canonical name; "
        "NAME=ls (default): list all",
    )
    add_name_list_flags(dynamic_substitution_parser)
    add_verbose_arguments(dynamic_substitution_parser)
    track_given_flags(dynamic_substitution_parser, NAME_LIST_DESTS)

    dynamic_substitution_parser.set_defaults(func=_dynamic_substitution_main)
