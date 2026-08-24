"""
list_variant_parser.py

define ``register_list_variant_parser``
"""

from kaye_engine.cli.cli_setup_guard import check_corpus_setup_for_cli
from kaye_engine.prompt.affordance_registry import variant_registry

# constants  ###################################################################
_HELP = "list names of all registered variants"

_DESCRIPTION = _HELP + """

prints the canonical name of each registered variant in
variant_registry, sorted alphabetically, one per line"""


# auxiliaries  #################################################################
def _list_variant_main(_):
    check_corpus_setup_for_cli()

    for variant_name in sorted(variant_registry):
        print(variant_name)


# Public API  ##################################################################
def register_list_variant_parser(cli_subparser):
    """
    register the ``kaye-engine list-variant``/``lsv`` subcommand parser
    """
    list_variant_parser = cli_subparser.add_parser(
        "list-variant",
        aliases=["lsv"],
        help=_HELP,
        description=_DESCRIPTION,
    )

    list_variant_parser.set_defaults(func=_list_variant_main)
