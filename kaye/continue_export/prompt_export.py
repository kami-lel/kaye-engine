"""
prompt_export.py

define ``export_prompts``
"""

from pathlib import Path

from kaye.prompt.prompt_blueprint import PromptBlueprint

from kaye.continue_export.rule_file import RuleFile

# blueprints  ##################################################################


_prompt_node = PromptBlueprint.create_empty_blueprint().corpus["Continue"][
    "Continue Prompts"
]


# maintain changelog
changelog_blueprint = PromptBlueprint.create_empty_blueprint()
changelog_blueprint.checkmark(_prompt_node["maintain CHANGELOG"])
changelog_blueprint.display_name = "maintain CHANGELOG"


# constants  ###################################################################


FILENAME2BLUEPRINT = {"maintain_changelog": changelog_blueprint}


# Entry Point  #################################################################
def export_prompts(prompts_folder):
    """
    export all prompts as Continue AI rule files

    iterates through ``FILENAME2BLUEPRINT`` and writes each prompt
    to a rule file in the destination folder, setting ``always_apply``
    to ``False`` and ``invokable`` to ``True`` for prompt invocation


    :param prompts_folder: destination folder for prompt rule files
    :type prompts_folder: Path-like
    """
    folder = Path(prompts_folder).resolve()
    folder.mkdir(parents=True, exist_ok=True)

    for k, bp in FILENAME2BLUEPRINT.items():
        filename = k + ".md"
        file_path = prompts_folder / filename

        print("update prompt:\t{}".format(filename))

        with RuleFile(file_path, encoding="utf-8") as rule:
            rule.name = bp.display_name
            rule.description = bp.description
            rule.always_apply = False
            rule.invokable = True
            rule.write_prefix()
            rule.write(bp.generate_prompt())
