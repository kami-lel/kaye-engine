"""
main_parser.py

define ``register_cli_blueprint_parser``
"""

from kaye_engine.cli.blueprint.generate_parser import register_generate_parser
from kaye_engine.cli.blueprint.list_parser import register_list_parser
from kaye_engine.cli.blueprint.preview_parser import register_preview_parser
from kaye_engine.cli.blueprint.show_parser import register_show_parser

# constants  ###################################################################
_HELP = "inspect and generate from registered prompt blueprints"


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

    cli_blueprint_parser.set_defaults(
        func=lambda _: cli_blueprint_parser.print_help()
    )

    cli_blueprint_subparser = cli_blueprint_parser.add_subparsers(
        description="operations available on registered prompt blueprints"
    )

    register_list_parser(cli_blueprint_subparser)
    register_preview_parser(cli_blueprint_subparser)
    register_show_parser(cli_blueprint_subparser)
    register_generate_parser(cli_blueprint_subparser)
