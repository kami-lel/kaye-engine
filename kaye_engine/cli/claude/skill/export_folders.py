"""
export_folders.py

define ``export_skills_as_folders``
"""

from kaye_engine import kamilog
from kaye_engine.cli.claude import LOGGER_CLAUDE_NAME
from kaye_engine.exportable import exportable_registry
from .skill_md import Skill

# logger  ######################################################################
logger = kamilog.getLogger(LOGGER_CLAUDE_NAME)

# entry point  #################################################################


def export_skills_as_folders(parent_folder, *, version, render_profile=None):
    """
    export every `exportable_registry` entry as a skill folder

    writes one subfolder per blueprint and per abbreviation group under
    ``parent_folder``


    :param parent_folder: destination directory to write skill folders into
    :type parent_folder: Path-like
    :param version: installed package version
    :type version: str
    :param render_profile: render options forwarded to
            :meth:`Skill.from_exportable`
    :type render_profile: RenderProfile, optional
    """
    logger.enter("exporting exportables as skills")

    for exportable in exportable_registry.values():
        try:
            folder = Skill.from_exportable(
                exportable, version=version, render_profile=render_profile
            ).write(parent_folder)
        except OSError as err:
            logger.critical("cannot write skill:\t" + exportable.display_name)
            raise SystemExit(1) from err
        logger.succ("export skill:\t{}".format(folder))
