"""export Kaye blueprints as Anthropic Claude Skill / Plugin"""

from kaye.cli.claude.code.parser import register_parser as register_code
from kaye.cli.claude.marketplace.parser import register_parser as register_marketplace
from kaye.cli.claude.plugin.parser import register_parser as register_plugin
from kaye.cli.claude.skill.parser import register_parser as register_skill
from kaye.cli.claude.vs_code.parser import register_parser as register_vs_code
from kaye.cli.claude.user_prompt.parser import register_parser as register_user_prompt


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

    register_code(claude_subparser)
    register_marketplace(claude_subparser)
    register_plugin(claude_subparser)
    register_skill(claude_subparser)
    register_vs_code(claude_subparser)
    register_user_prompt(claude_subparser)
