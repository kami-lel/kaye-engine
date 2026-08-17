"""
glossary_parser.py

define ``register_glossary_parser``
"""

from argparse import RawDescriptionHelpFormatter

from kaye_engine import LOGGER_NAME, kamilog
from kaye_engine.abbr_collection import abbr_glossary_registry, get_abbr_glossary
from kaye_engine.cli.cli_setup_guard import check_corpus_setup_for_cli
from kaye_engine.kamilog import (
    add_verbose_arguments,
    set_logging_level_by_namespace,
)
from kaye_engine.prompt.dynamic_nodes import gen_glossary_content_lines

# logger  ######################################################################
logger = kamilog.getLogger(LOGGER_NAME)

# constants  ###################################################################
_HELP = "print a glossary's content, or list all glossaries"

_DESCRIPTION = _HELP + """

prints the content of the glossary registered under GLOSSARY:

    kaye-engine glossary my-glossary-name

list every registered glossary, sorted alphabetically:

    kaye-engine glossary ls
"""


# auxiliaries  #################################################################
def _glossary_main(args):
    set_logging_level_by_namespace(args, logger=logger)
    check_corpus_setup_for_cli()

    if args.GLOSSARY == "ls":
        for name in sorted(abbr_glossary_registry):
            print(name)
        return

    try:
        get_abbr_glossary(args.GLOSSARY)
    except KeyError as err:
        logger.critical("unknown abbr glossary:\t" + args.GLOSSARY)
        raise SystemExit(1) from err

    print("\n".join(gen_glossary_content_lines(args.GLOSSARY)))


# Public API  ##################################################################
def register_glossary_parser(cli_subparser):
    """
    register the ``kaye-engine glossary`` subcommand parser
    """
    glossary_parser = cli_subparser.add_parser(
        "glossary",
        help=_HELP,
        description=_DESCRIPTION,
        formatter_class=RawDescriptionHelpFormatter,
        aliases=["g"],
    )

    # add arguments  -------------------------------------------------------
    glossary_parser.add_argument(
        "GLOSSARY",
        help="abbr glossary name; GLOSSARY=ls: list all glossaries",
    )
    add_verbose_arguments(glossary_parser)

    glossary_parser.set_defaults(func=_glossary_main)
