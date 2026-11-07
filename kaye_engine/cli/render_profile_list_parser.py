"""
render_profile_list_parser.py

define ``register_render_profile_list_parser``
"""

from kaye_engine.cli.list_view import (
    FMT_TABLE,
    add_list_flags,
    filter_rows,
    print_cards,
    print_rows,
    select_columns,
)
from kaye_engine.prompt.blueprint.render_profile_registry import (
    render_profile_registry,
)

# constants  ###################################################################
_HELP = "list all registered render profiles"

_DESCRIPTION = _HELP + """

prints each registered render profile in render_profile_registry, sorted
alphabetically, as an aligned table: `profile`, `variants` and `sidecars`
as counts, `remark`; `-c` picks columns from `remark`, `mode`,
`sparseness`, `variants`, `sidecars`; `-l` prints one detail card per
profile with every list in full; `-r PATTERN` keeps matching names; `-f`
picks table, tsv or json; `-N` prints names only. Piped output is tsv,
with lists comma-joined"""

# every column key `-c` accepts, in card order
_ALL_COLUMNS = ("remark", "mode", "sparseness", "variants", "sidecars")

# columns of the default table; remark last so its width never pushes others
_DFT_COLUMNS = ("variants", "sidecars", "remark")

# card fields in print order; remark is the card title, not a field
_CARD_COLUMNS = ("mode", "sparseness", "variants", "sidecars")


# auxiliaries  #################################################################
def _build_cells(entry):
    """
    :return: ``entry``'s columns as raw values, keyed like
            ``_ALL_COLUMNS``; ``variants`` and ``sidecars`` stay lists
    :rtype: dict
    """
    profile = entry.profile
    return {
        "remark": entry.remark,
        "mode": profile.mode.name or str(profile.mode),
        "sparseness": profile.sparseness,
        "variants": list(profile.variants or ()),
        "sidecars": list(profile.conditional_sidecars),
    }


def _build_list_field(label, names):
    """
    :return: a card field for a plain name list: its count, then the names
    :rtype: tuple
    """
    if not names:
        return (label, "(0)")
    return (label, "({})".format(len(names)), names)


def _build_sidecar_field(cells):
    """
    :return: the ``sidecars`` card field; sidecars that only echo a
            variant as ``[variant]`` fold into one phrase, so the names
            below it are the ones the variants do not imply
    :rtype: tuple
    """
    sidecars = cells["sidecars"]
    echoed = {"[{}]".format(name) for name in cells["variants"]}
    extra = [name for name in sidecars if name not in echoed]
    if len(extra) == len(sidecars):
        return _build_list_field("sidecars", sidecars)

    summary = "({}): the variants in [ ]".format(len(sidecars))
    if not extra:
        return ("sidecars", summary)
    return ("sidecars", summary + ", plus", extra)


def _build_card_fields(cells, keys):
    """
    :param keys: card columns to include
    :type keys: collections.abc.Container[str]
    :return: the card's fields, in ``_CARD_COLUMNS`` order
    :rtype: list[tuple]
    """
    builders = {
        "mode": lambda: ("mode", cells["mode"]),
        "sparseness": lambda: ("sparseness", str(cells["sparseness"])),
        "variants": lambda: _build_list_field("variants", cells["variants"]),
        "sidecars": lambda: _build_sidecar_field(cells),
    }
    return [builders[key]() for key in _CARD_COLUMNS if key in keys]


def _list_render_profile_main(args):
    rows = [
        (name, _build_cells(render_profile_registry[name]))
        for name in sorted(render_profile_registry)
    ]

    is_card_view = (
        args.long and not args.names_only and args.format in (None, FMT_TABLE)
    )
    if is_card_view:
        keys = set(select_columns(args, _ALL_COLUMNS))
        cards = (
            (name, cells["remark"], _build_card_fields(cells, keys))
            for name, cells in filter_rows(args, rows)
        )
        print_cards(args, cards)
        return

    columns = select_columns(args, _DFT_COLUMNS)
    print_rows(args, "profile", columns, rows)


# Public API  ##################################################################
def register_render_profile_list_parser(cli_subparser):
    """
    register the ``kaye-engine render-profile``/``rp`` subcommand parser
    """
    render_profile_list_parser = cli_subparser.add_parser(
        "render-profile",
        aliases=["rp"],
        help=_HELP,
        description=_DESCRIPTION,
    )

    add_list_flags(render_profile_list_parser, _ALL_COLUMNS)

    render_profile_list_parser.set_defaults(func=_list_render_profile_main)
