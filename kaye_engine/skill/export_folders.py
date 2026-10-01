"""
export_folders.py

define ``export_skills_as_folders``
"""

import kamilog
from kaye_engine.skill import LOGGER_SKILL_NAME
from .select import select_exportables
from .skill_md import Skill

# logger  ######################################################################
logger = kamilog.getLogger(LOGGER_SKILL_NAME)

# entry point  #################################################################


def export_skills_as_folders(
    parent_folder, *, version, render_profile=None, names=None
):
    """
    export `exportable_registry` entries as skill folders: every entry, or
    only those named

    writes one subfolder per blueprint and per abbreviation group under
    ``parent_folder``


    :param parent_folder: destination directory to write skill folders into
    :type parent_folder: Path-like
    :param version: installed package version
    :type version: str
    :param render_profile: render options forwarded to
            :meth:`Skill.from_exportable`
    :type render_profile: RenderProfile, optional
    :param names: canonical names to export; ``None`` exports every entry
    :type names: Iterable[str], optional
    :raises ValueError: 1+ names are not registered; nothing is written
    """
    exportables = select_exportables(names)
    logger.enter("exporting exportables as skills")

    for exportable in exportables:
        try:
            Skill.from_exportable(
                exportable, version=version, render_profile=render_profile
            ).write(parent_folder)
        except OSError as err:
            logger.critical("cannot write skill:\t" + exportable.display_name)
            raise SystemExit(1) from err
