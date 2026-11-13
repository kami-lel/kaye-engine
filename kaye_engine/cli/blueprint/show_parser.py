"""
show_parser.py

define ``register_show_parser``
"""

from argparse import RawDescriptionHelpFormatter

import kamilog
from kaye_engine.cli.verbosity import apply_verbosity_arg
from kaye_engine import LOGGER_NAME
from kaye_engine.cli.blueprint.aux_input import get_cmd_blueprint
from kaye_engine.cli.blueprint.aux_output import (
    emit_str,
    fmt_show_result,
    pick_show_fx,
    run_cmd_and_exit,
)
from kaye_engine.cli.blueprint.blueprint_arg_parser import (
    build_blueprint_arg_parser,
)
from kaye_engine.cli.cli_setup_guard import check_corpus_setup_for_cli
from kaye_engine.cli.list_view import make_renderer
from kamilog import (
    add_verbose_arguments,
)

# logger  ######################################################################
logger = kamilog.getLogger(LOGGER_NAME)

# constants  ###################################################################

_HELP = "show a blueprint's summary, or one of its fields"


_DESCRIPTION = _HELP + """

by default, prints the blueprint summary: banner-headed fields, in color on
a TTY (-C or NO_COLOR for plain)

with -F/--field, prints only that field, raw

select BLUEPRINT by canonical name in blueprint registry:

    kaye-engine blueprint show my-blueprint
    kaye-engine blueprint show my-blueprint --field globs

reading blueprint from stdin, a preview tree or JSON:

    kaye-engine blueprint show < my-blueprint.json
    cat my-tree.txt | kaye-engine blueprint show --field description
"""

# the fields ``--field`` selects: keys of ``SHOW_FIELD_FXS``
_FIELDS = (
    "display-name",
    "description",
    "description-node",
    "when-to-use",
    "when-to-use-node",
    "nodes",
    "subtrees",
    "globs",
    "dependencies",
)


# auxiliaries  #################################################################
def _show_main(args):
    apply_verbosity_arg(args)
    check_corpus_setup_for_cli()

    loaded = get_cmd_blueprint(args.BLUEPRINT)
    show_fx = pick_show_fx(args.field, renderer=make_renderer(args))

    emit_str(fmt_show_result(show_fx(loaded.blueprint)))


# Public API  ##################################################################
def register_show_parser(cli_subparser):
    """
    register the ``kaye blueprint show`` subcommand parser
    """
    show_parser = cli_subparser.add_parser(
        "show",
        help=_HELP,
        description=_DESCRIPTION,
        formatter_class=RawDescriptionHelpFormatter,
        aliases=["s"],
        parents=[build_blueprint_arg_parser()],
    )

    # add arguments  -----------------------------------------------------------
    show_parser.add_argument(
        "-F",
        "--field",
        choices=_FIELDS,
        default=None,
        metavar="FIELD",
        help="show one field alone, raw; one of: " + ", ".join(_FIELDS),
    )

    show_parser.add_argument(
        "-C",
        "--no-color",
        action="store_true",
        help="plain summary; NO_COLOR does the same",
    )

    add_verbose_arguments(show_parser)

    show_parser.set_defaults(
        func=lambda args: run_cmd_and_exit(_show_main, args)
    )
