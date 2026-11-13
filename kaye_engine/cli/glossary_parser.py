"""
glossary_parser.py

define ``register_glossary_parser``
"""

from argparse import RawDescriptionHelpFormatter

from kaye_engine.cli.verbosity import apply_verbosity_arg
from kaye_engine.abbr_collection import abbr_glossary_registry, get_abbr_glossary
from kaye_engine.cli.cli_error import report_unknown
from kaye_engine.cli.cli_setup_guard import check_corpus_setup_for_cli
from kaye_engine.cli.list_view import (
    NAME_LIST_DESTS,
    add_name_list_flags,
    print_names,
    reject_given_flags,
    track_given_flags,
)
from kamilog import (
    add_verbose_arguments,
)
from kaye_engine.prompt.dynamic_nodes import gen_glossary_content_lines

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
    apply_verbosity_arg(args)
    check_corpus_setup_for_cli()

    if args.GLOSSARY == "ls":
        print_names(args, "glossaries", sorted(abbr_glossary_registry))
        return

    reject_given_flags(args, NAME_LIST_DESTS, "entry mode")

    try:
        get_abbr_glossary(args.GLOSSARY)
    except KeyError:
        report_unknown("glossary", args.GLOSSARY, abbr_glossary_registry)

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
        nargs="?",
        default="ls",
        help="abbr glossary name; GLOSSARY=ls (default): list all glossaries",
    )
    add_name_list_flags(glossary_parser)
    add_verbose_arguments(glossary_parser)
    track_given_flags(glossary_parser, NAME_LIST_DESTS)

    glossary_parser.set_defaults(func=_glossary_main)
