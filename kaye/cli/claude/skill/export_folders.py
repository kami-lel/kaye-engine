"""
export_skills_as_folders.py

define ``export_skills_as_folders``
"""

from kaye import logger
from kaye.prompt.blueprint import BLUEPRINT_REGISTRIES
from kaye.cli.claude import convert_display_name2skill_name
from .skill_folder import AgentSkillFolder
from kaye.cli.exportable_abbr import EXPORTABLE_ABBRS

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
    for reg in BLUEPRINT_REGISTRIES.values():
        if not reg.skill_exportable:
            continue

        with AgentSkillFolder(parent_folder, registry=reg):
            pass

    logger.enter("exporting abbreviation groups as skills")

    # export abbrs
    for group in EXPORTABLE_ABBRS:
        skill_name = convert_display_name2skill_name(group.display_name)

        with AgentSkillFolder(parent_folder, skill_name=skill_name) as skill:
            skill.skill_md.description = group.description
            skill.skill_md.frontmatter["user-invocable"] = False
            skill.skill_md.write_frontmatter_part()
            skill.skill_md.write(group.as_md_list())
