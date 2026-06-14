"""export Kaye blueprints as single Anthropic Claude plugin"""

from kaye.cli.cli_claude.cli_claude_update import (
    register_cli_claude_update_parser,
)
from kaye.cli.cli_claude.cli_claude_create import (
    register_cli_claude_create_parser,
)


def register_cli_claude_parser(  ###############################################
    cli_subparser,
):  # pylint: disable=missing-function-docstring
    claude_parser = cli_subparser.add_parser(
        "claude",
        help=__doc__,
        description=__doc__,
        aliases=["anthropic", "a"],
    )

    def _claude_parser_main(_):
        claude_parser.print_help()

    claude_parser.set_defaults(func=_claude_parser_main)

    claude_subparser = claude_parser.add_subparsers(
        description="utility functions for the Claude plugin integration"
    )

    register_cli_claude_update_parser(claude_subparser)
    register_cli_claude_create_parser(claude_subparser)
