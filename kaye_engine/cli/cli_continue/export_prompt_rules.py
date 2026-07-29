"""
prompt_export.py

define ``export_prompts``
"""

from pathlib import Path

from kaye_engine import logger
from kaye_engine.prompt.blueprint import blueprint_registry
from kaye_engine.cli.cli_continue.rule_file import ContinueRule


# Entry Point  #################################################################
def export_prompt_rules(prompts_folder):
    """
    export all non-LLM-invokable, Continue-exportable blueprints as
    Continue Prompts files


    :param prompts_folder: destination folder for prompt rule files
    :type prompts_folder: Path-like
    """
    folder = Path(prompts_folder).resolve()
    folder.mkdir(parents=True, exist_ok=True)

    for reg in blueprint_registry.values():
        if not (reg.continue_exportable and not reg.llm_invokable):
            continue

        filename = reg.display_name + ".md"
        file_path = folder / filename

        ContinueRule.from_registry(reg).write(file_path)

        logger.succ("prompt:\t{}".format(file_path))
