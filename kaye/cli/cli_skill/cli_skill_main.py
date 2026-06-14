"""export Kaye blueprints as agentskills.io-standard Skills (for Anthropic Claude)"""

from kaye.cli.cli_skill.cli_skill_update import register_cli_skill_update_parser
from kaye.cli.cli_skill.cli_skill_create import register_cli_skill_create_parser


def register_cli_skill_parser(  ################################################
    cli_subparser,
):  # pylint: disable=missing-function-docstring
    skill_parser = cli_subparser.add_parser(
        "skill", help=__doc__, description=__doc__, aliases=["s"]
    )

    def _skill_parser_main(_):
        skill_parser.print_help()

    skill_parser.set_defaults(func=_skill_parser_main)

    skill_subparser = skill_parser.add_subparsers(
        description="utility functions for the Skill integration"
    )

    register_cli_skill_update_parser(skill_subparser)
    register_cli_skill_create_parser(skill_subparser)
