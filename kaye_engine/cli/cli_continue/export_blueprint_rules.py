"""
blueprint_rule.py

define ``export_all_blueprint_rules``, the full pipeline for writing
blueprints as Continue AI rule files via ``ContinueRule``
"""

from pathlib import Path

from kaye_engine import logger
from kaye_engine.prompt.blueprint import BLUEPRINT_REGISTRIES

from kaye_engine.cli.cli_continue.rule_file import ContinueRule

# Entry Point  #################################################################


def export_blueprint_rules(rules_folder):
    """
    export all Continue-exportable, LLM-invokable blueprints as Continue AI
    rule files

    creates ``rules_folder`` if it does not exist, then writes one rule file
    per registry entry with ``continue_exportable`` and ``llm_invokable``
    set (excluding non-``llm_invokable`` entries, which belong to
    ``export_prompt_rules`` instead)


    :param rules_folder: destination folder for rule files
    :type rules_folder: Path-like
    """
    folder_path = Path(rules_folder).resolve()
    folder_path.mkdir(parents=True, exist_ok=True)

    for reg in BLUEPRINT_REGISTRIES.values():
        if not reg.continue_exportable or not reg.llm_invokable:
            continue

        file_path = folder_path / "{}.md".format(reg.display_name)

        ContinueRule.from_registry(reg).write(file_path)

        logger.succ("blueprint rule:\t{}".format(file_path))
