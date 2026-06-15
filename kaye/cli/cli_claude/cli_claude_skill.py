"""export Kaye blueprints as agentskills.io-standard Skills for Anthropic Claude"""

import shutil
import tempfile
from pathlib import Path

from kaye.cli.cli_claude.export_skills_as_folders import (
    export_skills_as_folders,
)

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
            folder.mkdir(parents=True, exist_ok=True)
            with (
                tempfile.TemporaryDirectory() as skills_temp,
                tempfile.TemporaryDirectory() as zips_temp,
            ):
                export_skills_as_folders(Path(skills_temp), verbose=False)

                for skill_folder in Path(skills_temp).iterdir():
                    zip_base = Path(zips_temp) / skill_folder.name
                    shutil.make_archive(
                        str(zip_base),
                        "zip",
                        root_dir=skill_folder.parent,
                        base_dir=skill_folder.name,
                    )

                for zip_file in Path(zips_temp).iterdir():
                    dest = folder / zip_file.name
                    shutil.move(str(zip_file), str(dest))
                    print(f"export skill:\t{dest}")
        else:
            export_skills_as_folders(folder)

    skill_parser.set_defaults(func=_skill_main)
