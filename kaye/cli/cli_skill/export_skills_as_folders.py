"""
export_skill.py

define ``export_skills_as_folders``
"""

from kaye.cli import EXPORTABLE_BLUEPRINTS
from kaye.cli.cli_skill import convert_display_name2skill_name

from kaye.cli.cli_skill.agent_skill_folder import AgentSkillFolder
from kaye.cli.prompts_blueprints import PROMPTS_BLUEPRINTS

# entry point  #################################################################


def export_skills_as_folders(parent_folder):
    # export embedded_blueprints and prompts
    for blueprint in EXPORTABLE_BLUEPRINTS + PROMPTS_BLUEPRINTS:
        print(
            "export skill:\t"
            + convert_display_name2skill_name(blueprint.display_name)
        )
        with AgentSkillFolder(parent_folder, blueprint=blueprint):
            pass

    # export abbrs
    # TODO export abbrs
