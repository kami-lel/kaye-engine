"""
exportable_parser.py

define ``register_export_parser``
"""

# Hack no test file cover CLI kaye x

from argparse import RawDescriptionHelpFormatter

from kaye_engine import LOGGER_NAME, kamilog
from kaye_engine.cli.cli_setup_guard import check_corpus_setup_for_cli
from kaye_engine.exportable import exportable_registry
from kaye_engine.kamilog import (
    add_verbose_arguments,
    set_logging_level_by_namespace,
)

# logger  ######################################################################
logger = kamilog.getLogger(LOGGER_NAME)

# constants  ###################################################################
_HELP = "print an exportable's content, or list all exportables"

_DESCRIPTION = _HELP + """

prints the content of the exportable registered under EXPORTABLE:

    kaye-engine export my-canonical-name

list every registered exportable, sorted alphabetically:

    kaye-engine export ls
"""


# auxiliaries  #################################################################
def _export_main(args):
    set_logging_level_by_namespace(args, logger=logger)
    check_corpus_setup_for_cli()

    if args.EXPORTABLE == "ls":
        for name in sorted(exportable_registry):
            print(name)
        return

    try:
        exportable = exportable_registry[args.EXPORTABLE]
    except KeyError as err:
        logger.critical("unknown exportable:\t" + args.EXPORTABLE)
        raise SystemExit(1) from err

    print(exportable.content())


# Public API  ##################################################################
def register_export_parser(cli_subparser):
    """
    register the ``kaye-engine export`` subcommand parser
    """
    export_parser = cli_subparser.add_parser(
        "export",
        help=_HELP,
        description=_DESCRIPTION,
        formatter_class=RawDescriptionHelpFormatter,
        aliases=["x"],
    )

    # add arguments  -------------------------------------------------------
    export_parser.add_argument(
        "EXPORTABLE",
        help="exportable canonical name; EXPORTABLE=ls: list all exportables",
    )
    add_verbose_arguments(export_parser)

    export_parser.set_defaults(func=_export_main)
