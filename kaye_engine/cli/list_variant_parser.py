"""
list_variant_parser.py

define ``register_list_variant_parser``
"""

import sys
from itertools import groupby

from kaye_engine.cli.cli_setup_guard import note_empty_registry_for_cli
from kaye_engine.cli.list_view import (
    FMT_JSON,
    FMT_TABLE,
    FMT_TSV,
    add_list_flags,
    filter_rows,
    parse_regex,
    print_cards,
    print_groups,
    print_rows,
    resolve_format,
    select_columns,
)
from kaye_engine.prompt.affordance_registry import variant_registry

# constants  ###################################################################
_HELP = "list all registered variants, grouped by affordance"

_DESCRIPTION = _HELP + """

prints each registered variant in variant_registry under a bold header per
affordance, sorted by affordance, then by variant name; `-F` prints one flat
table instead, with `affordance` and `remark` columns; `-c` picks columns
from `affordance` and `remark`, and implies a flat table; `-a PATTERN` keeps
variants of matching affordances; `-l` prints one card per variant; `-r
PATTERN` keeps matching variant names; `-f` picks table, tsv or json; `-N`
prints names only. Piped output is a flat tsv"""

# every column key `-c` accepts, in print order
_COLUMNS = ("affordance", "remark")

_VIEW_FLAT = "flat"
_VIEW_CARD = "card"
_VIEW_GROUP = "group"


# auxiliaries  #################################################################
def _build_rows(args):
    """
    :return: the variants kept by ``-r`` and ``-a``, as
            ``(name, cells)``, sorted by affordance, then name
    :rtype: list[tuple]
    """
    entries = sorted(
        variant_registry.values(),
        key=lambda entry: (entry.affordance_name, entry.canonical_name),
    )
    rows = [
        (
            entry.canonical_name,
            {
                "affordance": entry.affordance_name,
                "remark": entry.remark,
                "_entry": entry,
            },
        )
        for entry in entries
    ]
    rows = filter_rows(args, rows)
    return [
        row
        for row in rows
        if not args.affordance
        or any(pat.search(row[1]["affordance"]) for pat in args.affordance)
    ]


def _pick_view(args):
    """
    :return: grouped by affordance on a table meant for a person, unless
            flat, columns, cards, names only or a machine format say
            otherwise
    :rtype: str
    """
    if args.names_only or args.format in (FMT_TSV, FMT_JSON):
        return _VIEW_FLAT
    if args.long:
        return _VIEW_CARD
    is_table = resolve_format(args, sys.stdout) == FMT_TABLE
    if is_table and not args.flat and not args.columns:
        return _VIEW_GROUP
    return _VIEW_FLAT


def _build_card(name, cells):
    """
    :return: ``(title, remark, fields)`` of one variant's card
    :rtype: tuple
    """
    entry = cells["_entry"]
    return (
        name,
        cells["remark"],
        [
            ("affordance", entry.affordance_name),
            ("usage sidecar", entry.usage_sidecar_name),
            ("lack sidecar", entry.lack_sidecar_name),
        ],
    )


def _list_variant_main(args):
    if not variant_registry:
        note_empty_registry_for_cli("variants")

    rows = _build_rows(args)
    view = _pick_view(args)

    if view == _VIEW_CARD:
        print_cards(args, (_build_card(name, cells) for name, cells in rows))
    elif view == _VIEW_GROUP:
        groups = (
            (aff, [(name, cells["remark"]) for name, cells in members])
            for aff, members in groupby(
                rows, key=lambda row: row[1]["affordance"]
            )
        )
        print_groups(args, groups)
    else:
        columns = select_columns(args, _COLUMNS)
        print_rows(args, "variant", columns, rows)


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

    add_list_flags(list_variant_parser, _COLUMNS)
    list_variant_parser.add_argument(
        "-a",
        "--affordance",
        action="append",
        default=[],
        type=parse_regex,
        metavar="PATTERN",
        help="only variants of affordances matching PATTERN (regex search); "
        "repeat to match any of several",
    )
    list_variant_parser.add_argument(
        "-F",
        "--flat",
        action="store_true",
        help="one flat table with an affordance column, no grouping",
    )

    list_variant_parser.set_defaults(func=_list_variant_main)
