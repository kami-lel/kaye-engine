"""
render_profile_list_parser.py

define ``register_render_profile_list_parser``
"""

from kaye_engine.prompt.blueprint.render_profile_registry import (
    render_profile_registry,
)

# constants  ###################################################################
_HELP = "list names of all registered render profiles"

_DESCRIPTION = _HELP + """

prints the name of each registered render profile in
render_profile_registry, sorted alphabetically, one per line; by default
a tab-separated remark follows the name, `NAME:<TAB>REMARK`, and a
profile with no remark prints its bare name"""


# auxiliaries  #################################################################
def _list_render_profile_main(args):
    for name in sorted(render_profile_registry):
        remark = render_profile_registry[name].remark
        if args.show_remark and remark:
            print(name + ":\t" + remark)
        else:
            print(name)


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

    # add arguments  -----------------------------------------------------------
    render_profile_list_parser.add_argument(
        "-r",
        "--remark",
        dest="show_remark",
        action="store_true",
        default=True,
        help="print each profile's remark after its name (default)",
    )
    render_profile_list_parser.add_argument(
        "-R",
        "--no-remark",
        dest="show_remark",
        action="store_false",
        help="print names only",
    )

    render_profile_list_parser.set_defaults(func=_list_render_profile_main)
