"""
export_skill.py

define ``export_skills_as_folders``
"""

from kaye.cli import EXPORTABLE_BLUEPRINTS
from kaye.cli.cli_skill import convert_display_name2skill_name

from kaye.cli.cli_skill.agent_skill_folder import AgentSkillFolder
from kaye.cli.exportable_abbr import EXPORTABLE_ABBRS
from kaye.cli.prompts_blueprints import PROMPTS_BLUEPRINTS

# entry point  #################################################################


def export_skills_as_folders(parent_folder):
    # export embedded_blueprints and prompts
    for blueprint in EXPORTABLE_BLUEPRINTS + PROMPTS_BLUEPRINTS:
        with AgentSkillFolder(parent_folder, blueprint=blueprint, verbose=True):
            pass

    # export abbrs
    for group in EXPORTABLE_ABBRS:
        skill_name = convert_display_name2skill_name(group.display_name)

        with AgentSkillFolder(
            parent_folder, skill_name=skill_name, verbose=True
        ) as skill:
            skill.skill_md.description = group.description
            skill.skill_md.write_frontmatter_part()
            skill.skill_md.write(group.as_md_list())
