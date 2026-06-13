"""
prompt_export.py

define ``export_prompts``
"""

from pathlib import Path

from kaye.cli.prompts_blueprints import PROMPTS_BLUEPRINTS
from kaye.cli.cli_continue.rule_file import RuleFile


# Entry Point  #################################################################
def export_prompts(prompts_folder):
    """
    export all prompts as Continue Prompts files


    :param prompts_folder: destination folder for prompt rule files
    :type prompts_folder: Path-like
    """
    folder = Path(prompts_folder).resolve()
    folder.mkdir(parents=True, exist_ok=True)

    for bp in PROMPTS_BLUEPRINTS:
        filename = bp.display_name + ".md"
        file_path = prompts_folder / filename

        print("update prompt:\t{}".format(filename))

        with RuleFile(file_path, blueprint=bp) as rule:
            rule.always_apply = False
            rule.invokable = True
