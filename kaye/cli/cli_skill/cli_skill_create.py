"""create .zip Skill packages from Kaye blueprints"""

import shutil
import tempfile
from pathlib import Path

from kaye.cli.cli_skill.export_skills_as_folders import export_skills_as_folders

# Bug no version in some skill, print version in ALL skills print mode


def register_cli_skill_create_parser(  #########################################
    cli_subparser,
):  # pylint: disable=missing-function-docstring
    create_parser = cli_subparser.add_parser(
        "create", help=__doc__, description=__doc__, aliases=["c", "z"]
    )

    create_parser.add_argument(
        "folder",
        nargs="?",
        metavar="FOLDER",
        type=Path,
        default=Path.cwd(),
        help=(
            "folder path to place created Skill .zip files, "
            "default: current directory"
        ),
    )

    def _create_main(args):
        skills_folder = args.folder
        skills_folder.mkdir(parents=True, exist_ok=True)

        with (
            tempfile.TemporaryDirectory() as skills_temp,
            tempfile.TemporaryDirectory() as zips_temp,
        ):
            export_skills_as_folders(
                Path(skills_temp), verbose=False, includes_version=True
            )

            for skill_folder in Path(skills_temp).iterdir():
                zip_base = Path(zips_temp) / skill_folder.name
                shutil.make_archive(
                    str(zip_base),
                    "zip",
                    root_dir=skill_folder.parent,
                    base_dir=skill_folder.name,
                )

            for zip_file in Path(zips_temp).iterdir():
                dest = skills_folder / zip_file.name
                shutil.move(str(zip_file), str(dest))
                print(f"export skill:\t{dest}")

    create_parser.set_defaults(func=_create_main)
