"""
export_skills_as_zips.py

define ``export_skills_as_zips``
"""

import shutil
import tempfile
from pathlib import Path

from kaye.cli.cli_claude.export_skills_as_folders import (
    export_skills_as_folders,
)

# entry point  #################################################################


def export_skills_as_zips(parent_folder, *, verbose=True):
    """
    export all blueprints, prompts, and abbreviation groups as ``.zip`` files

    writes one ``.zip`` per skill under ``parent_folder``; each archive
    contains the skill folder at its root so agentskills.io can unpack it
    directly


    :param parent_folder: destination directory to write ``.zip`` files into
    :type parent_folder: Path-like
    :param verbose: print exported paths when ``True``
    :type verbose: bool
    """
    parent_folder = Path(parent_folder)
    parent_folder.mkdir(parents=True, exist_ok=True)

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
            dest = parent_folder / zip_file.name
            shutil.move(str(zip_file), str(dest))
            if verbose:
                print(f"export skill:\t{dest}")
