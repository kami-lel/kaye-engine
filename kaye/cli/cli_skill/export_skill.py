"""
export_skill.py

define ``export_skills_as_folders``
"""

from kaye.cli.cli_skill.agent_skill_folder import AgentSkillFolder
from kaye.cli.prompts_blueprints import PROMPTS_BLUEPRINTS


def _convert_display_name2skill_name(display_name):
    pass


def export_skills_as_folders(parent_folder):
    # TODO export embedded blueprints

    for blueprint in PROMPTS_BLUEPRINTS:
        with AgentSkillFolder(parent_folder) as skill:
            skill.skill_md.blueprint = blueprint

    # TODO export abbrs
    pass
