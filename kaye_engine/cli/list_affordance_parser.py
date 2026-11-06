"""
list_affordance_parser.py

define ``register_list_affordance_parser``
"""

from kaye_engine.cli.cli_setup_guard import check_corpus_setup_for_cli
from kaye_engine.cli.list_table import (
    add_info_flags,
    print_table,
    select_info_columns,
)
from kaye_engine.prompt.affordance_registry import affordance_registry

# constants  ###################################################################
_HELP = "list all registered affordances"

_DESCRIPTION = _HELP + """

prints each registered affordance in affordance_registry, sorted
alphabetically, as tab-separated columns under a heading line:
`affordance` and `remark`; `-I` prints names only, with no heading line"""

# column key -> its flags; `remark` has no flag of its own, `-i`/`-I` toggle it
_INFO_COLUMNS = {"remark": None}


# auxiliaries  #################################################################
def _list_affordance_main(args):
    check_corpus_setup_for_cli()

    selected = select_info_columns(args, _INFO_COLUMNS)
    rows = (
        (name, {"remark": affordance_registry[name].remark})
        for name in sorted(affordance_registry)
    )
    print_table("affordance", selected, rows)


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

    add_info_flags(list_affordance_parser, _INFO_COLUMNS)

    list_affordance_parser.set_defaults(func=_list_affordance_main)
