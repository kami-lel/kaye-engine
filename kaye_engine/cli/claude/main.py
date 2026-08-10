"""install Kaye into Claude as skills, plugins, or marketplaces"""

from kaye_engine.cli.claude.code.parser import register_code_parser
from kaye_engine.cli.claude.marketplace.parser import (
    register_marketplace_parser,
)
from kaye_engine.cli.claude.plugin.parser import register_plugin_parser
from kaye_engine.cli.claude.skill.parser import register_skill_parser
from kaye_engine.cli.claude.user_prompt.parser import (
    register_user_prompt_parser,
)
from kaye_engine.cli.claude.vs_code.parser import register_vs_code_parser


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

    register_skill_parser(claude_subparser)
    register_user_prompt_parser(claude_subparser)
    register_plugin_parser(claude_subparser)
    register_marketplace_parser(claude_subparser)
    register_vs_code_parser(claude_subparser)
    register_code_parser(claude_subparser)
