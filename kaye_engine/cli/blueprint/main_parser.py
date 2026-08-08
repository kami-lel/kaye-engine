"""
main_parser.py

define ``register_cli_prompt_parser``
"""

from kaye_engine.cli.blueprint.ls_parser import register_ls_parser
from kaye_engine.cli.blueprint.show_parser import register_show_parser
from kaye_engine.cli.blueprint.generate_parser import register_generate_parser

# constants  ###################################################################
_HELP = "list, preview, and generate system prompts from prompt blueprints"


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
        description="available prompt blueprint operations"
    )

    register_ls_parser(cli_blueprint_subparser)
    register_show_parser(cli_blueprint_subparser)
    register_generate_parser(cli_blueprint_subparser)
