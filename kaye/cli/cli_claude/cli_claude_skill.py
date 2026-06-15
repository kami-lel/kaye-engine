"""export Kaye blueprints as agentskills.io-standard Skills for Anthropic Claude"""

from pathlib import Path

from kaye.cli.cli_claude.export_skills_as_folders import export_skills_as_folders
from kaye.cli.cli_claude.export_skills_as_zips import export_skills_as_zips

# constants  ===================================================================

_DEFAULT_SKILLS_FOLDER = Path.home() / ".claude" / "skills"


def register_cli_claude_skill_parser(  #########################################
    cli_subparser,
):  # pylint: disable=missing-function-docstring
    skill_parser = cli_subparser.add_parser(
        "skill",
        help=__doc__,
        description=__doc__,
        aliases=["s"],
    )

    skill_parser.add_argument(
        "folder",
        nargs="?",
        metavar="FOLDER",
        type=Path,
        default=None,
        help="destination folder; default: ~/.claude/skills/",
    )

    skill_parser.add_argument(
        "-z",
        "--zip",
        action="store_true",
        dest="zip",
        help="create .zip Skill packages; FOLDER default: current directory",
    )

    def _skill_main(args):
        folder = args.folder
        if folder is None:
            folder = Path.cwd() if args.zip else _DEFAULT_SKILLS_FOLDER

        if args.zip:
            export_skills_as_zips(folder)
        else:
            export_skills_as_folders(folder)

    skill_parser.set_defaults(func=_skill_main)
