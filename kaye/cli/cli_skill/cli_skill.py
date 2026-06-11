"""export Kaye blueprints as agentskills.io-standard Skills (for Anthropic Claude)"""

from pathlib import Path

from kaye.cli.cli_skill.create_skill import create_skill


def register_cli_skill_parser(  ################################################
    cli_subparser,
):  # pylint: disable=missing-function-docstring

    parser = cli_subparser.add_parser(
        "skill", help=__doc__, description=__doc__, aliases=["s", "a"]
    )

    parser.add_argument(
        "folder",
        nargs="?",
        metavar="FOLDER",
        type=Path,
        default=Path.cwd(),
        help="folder path to place Skills",
    )

    def _parser_main(args):
        create_skill(args.folder)

    parser.set_defaults(func=_parser_main)

    # TODO 2 subcommands
