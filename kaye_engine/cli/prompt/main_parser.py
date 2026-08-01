"""
main_parser.py

define ``register_cli_prompt_parser``
"""

from kaye_engine.cli.prompt.ls_parser import register_ls_parser
from kaye_engine.cli.prompt.show_parser import register_show_parser
from kaye_engine.cli.prompt.generate_parser import register_generate_parser

# constants  ###################################################################
_HELP = "list, preview, and generate system prompts from prompt blueprints"


def register_cli_prompt_parser(cli_subparser):  ################################
    """
    register the ``kaye prompt`` subcommand parser
    """
    cli_prompt_parser = cli_subparser.add_parser(
        "prompt",
        help=_HELP,
        description=_HELP,
        aliases=["p"],
    )

    cli_prompt_parser.set_defaults(
        func=lambda _: cli_prompt_parser.print_help()
    )

    cli_prompt_subparser = cli_prompt_parser.add_subparsers(
        description="available prompt blueprint operations"
    )

    register_ls_parser(cli_prompt_subparser)
    register_show_parser(cli_prompt_subparser)
    register_generate_parser(cli_prompt_subparser)
