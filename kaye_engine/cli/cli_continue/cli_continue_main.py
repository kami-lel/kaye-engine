"""utilities for the Continue AI code editor integration"""

from kaye_engine.cli.cli_continue.cli_continue_config import (
    register_cli_continue_config_parser,
)
from kaye_engine.cli.cli_continue.cli_continue_prompt import (
    register_cli_continue_prompt_parser,
)


def register_cli_continue_parser(  #############################################
    cli_subparser,
):  # pylint: disable=missing-function-docstring
    continue_parser = cli_subparser.add_parser(
        "continue", help=__doc__, description=__doc__, aliases=["c"]
    )

    def _continue_parser_main(_):
        continue_parser.print_help()

    continue_parser.set_defaults(func=_continue_parser_main)

    continue_subparser = continue_parser.add_subparsers(
        description="utility functions for the Continue integration"
    )

    register_cli_continue_config_parser(continue_subparser)
    register_cli_continue_prompt_parser(continue_subparser)
