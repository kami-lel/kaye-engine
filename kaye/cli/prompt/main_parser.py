"""
main_parser.py

define ``register_cli_prompt_parser``
"""

from kaye.cli.prompt.ls_parser import register_ls_subparser
from kaye.cli.prompt.show_parser import register_show_subparser
from kaye.cli.prompt.generate_parser import register_generate_subparser

_HELP = (
    "dynamically generate system prompt with a prompt blueprint "
    "as a subset of the prompt corpus"
)


def register_cli_prompt_parser(cli_subparser):  ################################
    """register the ``kaye prompt`` subcommand parser"""
    cli_prompt_parser = cli_subparser.add_parser(
        "prompt",
        help=_HELP,
        description=_HELP,
        aliases=["p"],
    )

    def _cli_prompt_parser_main(_):
        # when calling ``python -m kaye prompt``
        cli_prompt_parser.print_help()

    cli_prompt_parser.set_defaults(func=_cli_prompt_parser_main)

    cli_prompt_subparser = cli_prompt_parser.add_subparsers(
        description="utility functions related to prompt generation"
    )

    register_ls_subparser(cli_prompt_subparser)
    register_show_subparser(cli_prompt_subparser)
    register_generate_subparser(cli_prompt_subparser)
