"""install Kaye into Claude as skills, plugins, or marketplaces"""

from kaye.cli.claude.code.parser import register_code_subparser
from kaye.cli.claude.marketplace.parser import register_marketplace_subparser
from kaye.cli.claude.plugin.parser import register_plugin_subparser
from kaye.cli.claude.skill.parser import register_skill_subparser
from kaye.cli.claude.vs_code.parser import register_vs_code_subparser
from kaye.cli.claude.user_prompt.parser import register_user_prompt_subparser

# Todo add prompt: gap review, resolve merge conflict, Plan for Step By Step


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

    register_skill_subparser(claude_subparser)
    register_user_prompt_subparser(claude_subparser)
    register_plugin_subparser(claude_subparser)
    register_marketplace_subparser(claude_subparser)
    register_vs_code_subparser(claude_subparser)
    register_code_subparser(claude_subparser)
