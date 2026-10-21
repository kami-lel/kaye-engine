"""
main_parser.py

define ``register_cli_blueprint_parser``
"""

from kaye_engine.cli.blueprint.aux_output import run_cmd_and_exit
from kaye_engine.cli.blueprint.list_parser import (
    _list_main,
    register_list_parser,
)
from kaye_engine.cli.blueprint.preview_parser import register_preview_parser
from kaye_engine.cli.blueprint.render_parser import register_render_parser
from kaye_engine.cli.blueprint.show_parser import register_show_parser
from kaye_engine.cli.blueprint.validate_parser import (
    register_validate_parser,
)

# constants  ###################################################################
_HELP = "operate with (registered or not) prompt blueprints"


def register_cli_blueprint_parser(cli_subparser):  #############################
    """
    register the ``kaye blueprint`` subcommand parser
    """
    cli_blueprint_parser = cli_subparser.add_parser(
        "blueprint",
        help=_HELP,
        description=_HELP,
        aliases=["bp"],
    )

    # bare ``blueprint`` behaves as ``blueprint list``
    cli_blueprint_parser.set_defaults(
        func=lambda args: run_cmd_and_exit(_list_main, args)
    )

    cli_blueprint_subparser = cli_blueprint_parser.add_subparsers(
        description="operations available on registered prompt blueprints"
    )

    register_list_parser(cli_blueprint_subparser)
    register_preview_parser(cli_blueprint_subparser)
    register_show_parser(cli_blueprint_subparser)
    register_render_parser(cli_blueprint_subparser)
    register_validate_parser(cli_blueprint_subparser)
