"""
export_skills_as_zips.py

define ``export_skills_as_zips``
"""

import shutil
import tempfile
from pathlib import Path

import kamilog
from kaye_engine.deed import format_size, quiet_deeds, track
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
    parent_folder, *, version, render_profile=None, names=None
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
    :param render_profile: render options forwarded to
            :func:`export_skills_as_folders`
    :type render_profile: RenderProfile, optional
    :param names: canonical names to export; ``None`` exports every entry
    :type names: Iterable[str], optional
    :raises ValueError: 1+ names are not registered; nothing is written
    :return: number of ``.zip`` files exported
    :rtype: int
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
        return _report_zips_without_writing(
            parent_folder, version, render_profile, exportables
        )

    with tempfile.TemporaryDirectory() as skills_temp:
        logger.debug("building skill folders in temporary directory")
        with quiet_deeds():
            export_skills_as_folders(
                Path(skills_temp),
                version=version,
                render_profile=render_profile,
                names=[e.canonical_name for e in exportables],
            )

        logger.debug("archiving skills to .zip packages")
        skill_folders = sorted(Path(skills_temp).iterdir())
        for skill_folder in skill_folders:
            dest = parent_folder / (skill_folder.name + ".zip")
            try:
                with track(logger).create_zip("skill", dest) as deed:
                    shutil.make_archive(
                        str(parent_folder / skill_folder.name),
                        "zip",
                        root_dir=skill_folder.parent,
                        base_dir=skill_folder.name,
                    )
                    deed.stats = format_size(dest.stat().st_size)
            except (OSError, shutil.Error) as err:
                raise SystemExit(1) from err
    return len(skill_folders)


# auxiliaries  #################################################################
def _report_zips_without_writing(
    parent_folder, version, render_profile, exportables
):
    """
    log the result line of every skill archive, building and writing
    nothing -- the dry-run stand-in for the archive steps


    :return: number of ``.zip`` files that would be exported
    :rtype: int
    """
    logger.enter("exporting exportables as skills")
    for exportable in exportables:
        zip_name = (
            Skill.from_exportable(
                exportable, version=version, render_profile=render_profile
            ).name
            + ".zip"
        )
        with track(logger).create_zip(
            "skill", parent_folder / zip_name
        ) as deed:
            deed.stats = "size n/a"
    return len(exportables)
