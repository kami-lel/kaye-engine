"""update existing Skill folder with latest Kaye blueprints"""

from pathlib import Path

from kaye.cli.cli_skill.export_skills_as_folders import export_skills_as_folders

# constants  ===================================================================

_DEFAULT_SKILLS_FOLDER = Path.home() / ".claude" / "skills"


def register_cli_skill_update_parser(  #########################################
    cli_subparser,
):  # pylint: disable=missing-function-docstring
    update_parser = cli_subparser.add_parser(
        "update", help=__doc__, description=__doc__, aliases=["u"]
    )

    update_parser.add_argument(
        "folder",
        nargs="?",
        metavar="FOLDER",
        type=Path,
        default=_DEFAULT_SKILLS_FOLDER,
        help="skill folder path, default: ~/.claude/skills/",
    )

    def _update_main(args):
        export_skills_as_folders(args.folder)

    update_parser.set_defaults(func=_update_main)
