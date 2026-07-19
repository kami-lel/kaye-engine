"""
prompt_export.py

define ``export_prompts``
"""

from pathlib import Path

from kaye import logger
from kaye.prompt.blueprint import BLUEPRINT_REGISTRIES
from kaye.cli.cli_continue.rule_file import RuleFile


# Entry Point  #################################################################
def export_prompt_rules(prompts_folder):
    """
    export all invokable, Continue-exportable blueprints as Continue Prompts
    files


    :param prompts_folder: destination folder for prompt rule files
    :type prompts_folder: Path-like
    """
    folder = Path(prompts_folder).resolve()
    folder.mkdir(parents=True, exist_ok=True)

    for reg in BLUEPRINT_REGISTRIES.values():
        if not (reg.continue_exportable and reg.invokable):
            continue

        filename = reg.display_name + ".md"
        file_path = prompts_folder / filename

        with RuleFile(file_path, registry=reg):
            pass

        logger.succ("prompt:\t{}".format(file_path))
