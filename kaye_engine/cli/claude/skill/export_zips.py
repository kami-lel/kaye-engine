"""
export_skills_as_zips.py

define ``export_skills_as_zips``
"""

import shutil
import tempfile
from pathlib import Path

from kaye_engine import kamilog
from kaye_engine.cli.claude import LOGGER_CLAUDE_NAME
from kaye_engine.cli.claude.setup import get_claude_cli_consumer_version


from .export_folders import (
    export_skills_as_folders,
)

# logger  ######################################################################
logger = kamilog.getLogger(LOGGER_CLAUDE_NAME)

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
    try:
        parent_folder.mkdir(parents=True, exist_ok=True)
    except OSError as err:
        logger.critical(
            "cannot create destination folder:\t" + str(parent_folder)
        )
        raise SystemExit(1) from err

    pkg_version = get_claude_cli_consumer_version()

    with (
        tempfile.TemporaryDirectory() as skills_temp,
        tempfile.TemporaryDirectory() as zips_temp,
    ):
        logger.debug("building skill folders in temporary directory")
        export_skills_as_folders(Path(skills_temp), version=pkg_version)

        logger.debug("archiving skills to .zip packages")
        for skill_folder in Path(skills_temp).iterdir():
            logger.debug("archiving skill:\t{}".format(skill_folder.name))
            zip_base = Path(zips_temp) / skill_folder.name
            try:
                shutil.make_archive(
                    str(zip_base),
                    "zip",
                    root_dir=skill_folder.parent,
                    base_dir=skill_folder.name,
                )
            except (OSError, shutil.Error) as err:
                logger.critical(
                    "cannot archive skill:\t" + skill_folder.name
                )
                raise SystemExit(1) from err

        logger.debug("moving archived skills to destination folder")
        for zip_file in Path(zips_temp).iterdir():
            dest = parent_folder / zip_file.name
            try:
                shutil.move(str(zip_file), str(dest))
            except (OSError, shutil.Error) as err:
                logger.critical(
                    "cannot move archived skill to destination:\t"
                    + str(dest)
                )
                raise SystemExit(1) from err

            logger.succ("export skill:\t{}".format(dest))
