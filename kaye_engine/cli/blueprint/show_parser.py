"""
show_parser.py

define ``register_show_parser``
"""

from argparse import RawDescriptionHelpFormatter

import kamilog
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
from kamilog import (
    add_verbose_arguments,
    set_logging_level_by_namespace,
)

# logger  ######################################################################
logger = kamilog.getLogger(LOGGER_NAME)

# constants  ###################################################################

_HELP = "show a blueprint's summary, or one of its fields"


_DESCRIPTION = _HELP + """

by default, prints the blueprint summary

with a field flag, prints only that field; the flags are mutually exclusive

select BLUEPRINT by canonical name in blueprint registry:

    kaye-engine blueprint show my-blueprint
    kaye-engine blueprint show my-blueprint --globs

reading blueprint from stdin, a preview tree or JSON:

    kaye-engine blueprint show < my-blueprint.json
    cat my-tree.txt | kaye-engine blueprint show --description
"""

# (short flag or None, field): the field names a key of ``SHOW_FIELD_FXS``
_FIELD_FLAGS = (
    ("-n", "display-name"),
    ("-d", "description"),
    ("-w", "when-to-use"),
    ("-g", "globs"),
    ("-p", "dependencies"),
)


# auxiliaries  #################################################################
def _show_main(args):
    set_logging_level_by_namespace(args, logger=logger)
    check_corpus_setup_for_cli()

    loaded = get_cmd_blueprint(args.BLUEPRINT)
    show_fx = pick_show_fx(args.field)

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
    field_group = show_parser.add_mutually_exclusive_group()
    for short_flag, field in _FIELD_FLAGS:
        field_group.add_argument(
            *([short_flag] if short_flag else []),
            "--" + field,
            dest="field",
            action="store_const",
            const=field,
            default=None,
            help="show {} alone".format(field),
        )

    add_verbose_arguments(show_parser)

    show_parser.set_defaults(
        func=lambda args: run_cmd_and_exit(_show_main, args)
    )
