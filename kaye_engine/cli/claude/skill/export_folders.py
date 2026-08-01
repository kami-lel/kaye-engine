"""
export_folders.py

define ``export_skills_as_folders``
"""

from kaye_engine import kamilog
from kaye_engine.cli.claude import LOGGER_CLAUDE_NAME
from kaye_engine.prompt.blueprint import blueprint_registry
from kaye_engine.cli.exportable_abbr import EXPORTABLE_ABBRS
from .skill_md import Skill

# logger  ######################################################################
logger = kamilog.getLogger(LOGGER_CLAUDE_NAME)

# entry point  #################################################################


def export_skills_as_folders(parent_folder):
    """
    export all blueprints, prompts, and abbreviation groups as skill folders

    writes one subfolder per blueprint and per abbreviation group under
    ``parent_folder``; abbreviation skills are marked as non-user-invocable


    :param parent_folder: destination directory to write skill folders into
    :type parent_folder: Path-like
    """
    logger.enter("exporting blueprints and prompts as skills")

    # export blueprints and prompts
    for reg in blueprint_registry.values():
        if not reg.skill_exportable:
            continue

        try:
            folder = Skill.from_registry(reg).write(parent_folder)
        except OSError as err:
            logger.critical("cannot write skill:\t" + reg.display_name)
            raise SystemExit(1) from err
        logger.succ("export skill:\t{}".format(folder))

    logger.enter("exporting abbreviation groups as skills")

    # export abbrs
    for group in EXPORTABLE_ABBRS:
        folder = Skill(
            name=group.skill_name,
            description=group.description,
            user_invocable=False,
            body=group.as_md_list(),
        ).write(parent_folder)
        logger.succ("export skill:\t{}".format(folder))
