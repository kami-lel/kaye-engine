"""export Kaye blueprints as Anthropic Claude Skill / Plugin"""

from kaye.cli.cli_claude.claude_code.cli_claude_code import (
    register_cli_claude_code_parser,
)
from kaye.cli.cli_claude.claude_marketplace.cli_claude_marketplace import (
    register_cli_claude_marketplace_parser,
)
from kaye.cli.cli_claude.claude_plugin.cli_claude_plugin import (
    register_cli_claude_plugin_parser,
)
from kaye.cli.cli_claude.claude_skill.cli_claude_skill import (
    register_cli_claude_skill_parser,
)
from kaye.cli.cli_claude.claude_vs_code_extension.cli_claude_vs_code_extension import (
    register_cli_claude_vs_code_extension_parser,
)
from kaye.cli.cli_claude.user_prompt.cli_claude_user_prompt import (
    register_cli_claude_user_prompt_parser,
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

    register_cli_claude_code_parser(claude_subparser)
    register_cli_claude_marketplace_parser(claude_subparser)
    register_cli_claude_plugin_parser(claude_subparser)
    register_cli_claude_skill_parser(claude_subparser)
    register_cli_claude_vs_code_extension_parser(claude_subparser)
    register_cli_claude_user_prompt_parser(claude_subparser)
