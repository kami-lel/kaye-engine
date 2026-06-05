"""
prompt_export.py

define ``export_prompts``
"""

from kaye.prompt.prompt_blueprint import PromptBlueprint

from kaye.continue_export.rule_file import RuleFile

# blueprints  ##################################################################


_prompt_node = PromptBlueprint.create_empty_blueprint().corpus["Continue"][
    "Continue Prompts"
]


# constants  ###################################################################


FILENAME2BLUEPRINT = {"maintain_changelog": None}  # TODO


# Entry Point  #################################################################
def export_prompts(prompts_folder):
    for filename, bp in FILENAME2BLUEPRINT.items():
        file_path = prompts_folder / filename / ".md"

        print("update prompt:\t{}".format(file_path))

        with RuleFile(file_path, encoding="utf-8") as rule:
            rule.name = bp.display_name
            rule.description = bp.description
            rule.always_apply = False
            rule.invokable = True
            rule.write_prefix()
            rule.write(bp.generate_prompt())
