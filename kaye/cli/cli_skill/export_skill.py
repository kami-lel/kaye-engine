"""
export_skill.py

define ``export_skills_as_folders``
"""

from kaye.cli import EXPORTABLE_BLUEPRINTS

from kaye.cli.cli_skill.agent_skill_folder import AgentSkillFolder
from kaye.cli.prompts_blueprints import PROMPTS_BLUEPRINTS

# entry point  #################################################################


def export_skills_as_folders(parent_folder):
    # export embedded_blueprints and prompts
    for blueprint in EXPORTABLE_BLUEPRINTS + PROMPTS_BLUEPRINTS:
        print("export skill:\t" + blueprint.skill_name)
        with AgentSkillFolder(parent_folder, blueprint=blueprint):
            pass

    # TODO export abbrs
