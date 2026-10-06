"""
export_skills_as_zips.py

define ``export_skills_as_zips``
"""

import shutil
import tempfile
from pathlib import Path

import kamilog
from kaye_engine.deed import track
from kaye_engine.skill import LOGGER_SKILL_NAME
from kaye_engine.cli.dry_run import is_dry_run


from .export_folders import (
    export_skills_as_folders,
)
from .select import select_exportables
from .skill_md import Skill

# logger  ######################################################################
logger = kamilog.getLogger(LOGGER_SKILL_NAME)

# entry point  #################################################################


def export_skills_as_zips(
    parent_folder, *, version, verbose=True, render_profile=None, names=None
):
    """
    export all blueprints, prompts, and abbreviation groups as ``.zip`` files

    writes one ``.zip`` per skill under ``parent_folder``; each archive
    contains the skill folder at its root so agentskills.io can unpack it
    directly


    :param parent_folder: destination directory to write ``.zip`` files into
    :type parent_folder: Path-like
    :param version: installed package version
    :type version: str
    :param verbose: print exported paths when ``True``
    :type verbose: bool
    :param render_profile: render options forwarded to
            :func:`export_skills_as_folders`
    :type render_profile: RenderProfile, optional
    :param names: canonical names to export; ``None`` exports every entry
    :type names: Iterable[str], optional
    :raises ValueError: 1+ names are not registered; nothing is written
    """
    exportables = select_exportables(names)
    parent_folder = Path(parent_folder)
    try:
        with track(logger).create_dir(parent_folder):
            if not is_dry_run():
                parent_folder.mkdir(parents=True, exist_ok=True)
    except OSError as err:
        raise SystemExit(1) from err

    if is_dry_run():
        _report_zips_without_writing(
            parent_folder, version, render_profile, exportables
        )
        return

    with (
        tempfile.TemporaryDirectory() as skills_temp,
        tempfile.TemporaryDirectory() as zips_temp,
    ):
        logger.debug("building skill folders in temporary directory")
        export_skills_as_folders(
            Path(skills_temp),
            version=version,
            render_profile=render_profile,
            names=[e.canonical_name for e in exportables],
        )

        logger.debug("archiving skills to .zip packages")
        for skill_folder in Path(skills_temp).iterdir():
            zip_base = Path(zips_temp) / skill_folder.name
            try:
                with track(logger).pack_files(
                    skill_folder.name, zip_base.name + ".zip"
                ):
                    shutil.make_archive(
                        str(zip_base),
                        "zip",
                        root_dir=skill_folder.parent,
                        base_dir=skill_folder.name,
                    )
            except (OSError, shutil.Error) as err:
                raise SystemExit(1) from err

        logger.debug("moving archived skills to destination folder")
        for zip_file in Path(zips_temp).iterdir():
            dest = parent_folder / zip_file.name
            try:
                with track(logger).mv_file(zip_file.name, dest):
                    shutil.move(str(zip_file), str(dest))
            except (OSError, shutil.Error) as err:
                raise SystemExit(1) from err


# auxiliaries  #################################################################
def _report_zips_without_writing(
    parent_folder, version, render_profile, exportables
):
    """
    log the pack and move deeds of every skill archive, building and
    writing nothing -- the dry-run stand-in for the archive steps
    """
    logger.enter("exporting exportables as skills")
    for exportable in exportables:
        zip_name = (
            Skill.from_exportable(
                exportable, version=version, render_profile=render_profile
            ).name
            + ".zip"
        )
        with track(logger).pack_files(zip_name[:-4], zip_name):
            pass
        with track(logger).mv_file(zip_name, parent_folder / zip_name):
            pass
