"""
list_affordance_parser.py

define ``register_list_affordance_parser``
"""

from kamilog import add_verbose_arguments

from kaye_engine.cli.verbosity import apply_verbosity_arg
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
alphabetically, as an aligned table: `affordance`, `variant_count` of the
variants implementing it, `description`; `-c` picks columns from
`variant_count`, `variants` (the names, comma-joined, an array in json) and
`description`; `-l` prints one card per affordance with its variants and
their descriptions beneath; `-r PATTERN` keeps matching names; `-f` picks
table, tsv or json; `-N` prints names only. The columns and their meaning
are the same in every format; only the default format follows the stream:
table on a TTY, tsv piped"""

# every column key `-c` accepts, in print order
_COLUMNS = ("variant_count", "variants", "description")

# columns of the default table
_DFT_COLUMNS = ("variant_count", "description")


# auxiliaries  #################################################################
def _build_variant_ls(name):
    """
    :return: the variants implementing affordance ``name``, as
            ``(variant name, description)``, sorted by name
    :rtype: list[tuple]
    """
    return sorted(
        (entry.canonical_name, entry.remark)
        for entry in variant_registry.values()
        if entry.affordance_name == name
    )


def _list_affordance_main(args):
    apply_verbosity_arg(args)
    if not affordance_registry:
        note_empty_registry_for_cli("affordances")

    rows = []
    for name in sorted(affordance_registry):
        variants = _build_variant_ls(name)
        rows.append(
            (
                name,
                {
                    "variant_count": len(variants),
                    "variants": [variant for variant, _ in variants],
                    "description": affordance_registry[name].remark,
                    "_variants": variants,
                },
            )
        )

    is_card_view = (
        args.long and not args.names_only and args.format in (None, FMT_TABLE)
    )
    if is_card_view:
        cards = (
            (name, cells["description"], cells["_variants"])
            for name, cells in filter_rows(args, rows)
        )
        print_cards(args, cards, heading="affordances")
        return

    columns = select_columns(args, _DFT_COLUMNS)
    print_rows(
        args, "affordance", columns, rows, heading="affordances"
    )


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
    add_verbose_arguments(list_affordance_parser)

    list_affordance_parser.set_defaults(func=_list_affordance_main)
