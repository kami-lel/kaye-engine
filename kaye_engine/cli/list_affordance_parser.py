"""
list_affordance_parser.py

define ``register_list_affordance_parser``
"""

from kaye_engine.cli.cli_setup_guard import note_empty_registry_for_cli
from kaye_engine.cli.list_view import (
    FMT_TABLE,
    add_list_flags,
    filter_rows,
    print_cards,
    print_rows,
    select_columns,
)
from kaye_engine.prompt.affordance_registry import (
    affordance_registry,
    variant_registry,
)

# constants  ###################################################################
_HELP = "list all registered affordances"

_DESCRIPTION = _HELP + """

prints each registered affordance in affordance_registry, sorted
alphabetically, as an aligned table: `affordance`, `variants` as a count of
the variants implementing it, `remark`; `-c` picks columns from `variants`
and `remark`; `-l` prints one card per affordance with its variants and
their remarks beneath; `-r PATTERN` keeps matching names; `-f` picks table,
tsv or json; `-N` prints names only. Piped output is tsv, with variants
comma-joined"""

# every column key `-c` accepts, in print order
_COLUMNS = ("variants", "remark")


# auxiliaries  #################################################################
def _build_variant_ls(name):
    """
    :return: the variants implementing affordance ``name``, as
            ``(variant name, remark)``, sorted by name
    :rtype: list[tuple]
    """
    return sorted(
        (entry.canonical_name, entry.remark)
        for entry in variant_registry.values()
        if entry.affordance_name == name
    )


def _list_affordance_main(args):
    if not affordance_registry:
        note_empty_registry_for_cli("affordances")

    rows = []
    for name in sorted(affordance_registry):
        variants = _build_variant_ls(name)
        rows.append(
            (
                name,
                {
                    "variants": [variant for variant, _ in variants],
                    "remark": affordance_registry[name].remark,
                    "_variants": variants,
                },
            )
        )

    is_card_view = (
        args.long and not args.names_only and args.format in (None, FMT_TABLE)
    )
    if is_card_view:
        cards = (
            (name, cells["remark"], cells["_variants"])
            for name, cells in filter_rows(args, rows)
        )
        print_cards(args, cards)
        return

    columns = select_columns(args, _COLUMNS)
    print_rows(args, "affordance", columns, rows)


# Public API  ##################################################################
def register_list_affordance_parser(cli_subparser):
    """
    register the ``kaye-engine affordance``/``afd`` subcommand
    parser
    """
    list_affordance_parser = cli_subparser.add_parser(
        "affordance",
        aliases=["afd"],
        help=_HELP,
        description=_DESCRIPTION,
    )

    add_list_flags(list_affordance_parser, _COLUMNS)

    list_affordance_parser.set_defaults(func=_list_affordance_main)
