"""
list_variant_parser.py

define ``register_list_variant_parser``
"""

from kaye_engine.cli.cli_setup_guard import check_corpus_setup_for_cli
from kaye_engine.cli.list_table import (
    add_info_flags,
    print_table,
    select_info_columns,
)
from kaye_engine.prompt.affordance_registry import variant_registry

# constants  ###################################################################
_HELP = "list all registered variants, grouped by affordance"

_DESCRIPTION = _HELP + """

prints each registered variant in variant_registry as tab-separated
columns under a heading line: `variant`, `affordance` (-a), `remark`
(-r); `-i` shows both info columns, the default, and `-I` prints names
only, with no heading line. Flags apply in the order given, so the last
one wins. Rows are sorted by affordance, then by variant name, whichever
columns show"""

# column key -> (short flag, long flag), in print order
_INFO_COLUMNS = {
    "affordance": ("-a", "--affordance"),
    "remark": ("-r", "--remark"),
}


# auxiliaries  #################################################################
def _list_variant_main(args):
    check_corpus_setup_for_cli()

    selected = select_info_columns(args, _INFO_COLUMNS)
    entries = sorted(
        variant_registry.values(),
        key=lambda entry: (entry.affordance_name, entry.canonical_name),
    )
    rows = (
        (
            entry.canonical_name,
            {"affordance": entry.affordance_name, "remark": entry.remark},
        )
        for entry in entries
    )
    print_table("variant", selected, rows)


# Public API  ##################################################################
def register_list_variant_parser(cli_subparser):
    """
    register the ``kaye-engine variant``/``var`` subcommand parser
    """
    list_variant_parser = cli_subparser.add_parser(
        "variant",
        aliases=["var"],
        help=_HELP,
        description=_DESCRIPTION,
    )

    add_info_flags(list_variant_parser, _INFO_COLUMNS)

    list_variant_parser.set_defaults(func=_list_variant_main)
