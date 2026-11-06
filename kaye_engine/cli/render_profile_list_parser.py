"""
render_profile_list_parser.py

define ``register_render_profile_list_parser``
"""

from kaye_engine.cli.list_table import (
    add_info_flags,
    print_table,
    select_info_columns,
)
from kaye_engine.prompt.blueprint.render_profile_registry import (
    render_profile_registry,
)

# constants  ###################################################################
_HELP = "list all registered render profiles"

_DESCRIPTION = _HELP + """

prints each registered render profile in render_profile_registry, sorted
alphabetically, as tab-separated columns under a heading line: `profile`,
`remark` (-r), `mode` (-m), `sparseness` (-s), `variants` (-v), `sidecars`
(-c); `-i` shows every info column, the default, and `-I` prints names
only, with no heading line. Flags apply in the order given, so the last
one wins. `variants` and `sidecars` are comma-joined names"""

# column key -> (short flag, long flag), in print order
_INFO_COLUMNS = {
    "remark": ("-r", "--remark"),
    "mode": ("-m", "--mode"),
    "sparseness": ("-s", "--sparseness"),
    "variants": ("-v", "--variants"),
    "sidecars": ("-c", "--sidecars"),
}


# auxiliaries  #################################################################
def _build_cells(entry):
    """
    :return: ``entry``'s info columns as cell text, keyed like
            ``_INFO_COLUMNS``
    :rtype: dict[str, str]
    """
    profile = entry.profile
    return {
        "remark": entry.remark,
        "mode": profile.mode.name or str(profile.mode),
        "sparseness": str(profile.sparseness),
        "variants": ",".join(profile.variants or ()),
        "sidecars": ",".join(profile.conditional_sidecars),
    }


def _list_render_profile_main(args):
    selected = select_info_columns(args, _INFO_COLUMNS)
    rows = (
        (name, _build_cells(render_profile_registry[name]))
        for name in sorted(render_profile_registry)
    )
    print_table("profile", selected, rows)


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

    add_info_flags(render_profile_list_parser, _INFO_COLUMNS)

    render_profile_list_parser.set_defaults(func=_list_render_profile_main)
