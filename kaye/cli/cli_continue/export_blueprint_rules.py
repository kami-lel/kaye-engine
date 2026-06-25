"""
blueprint_rule.py

define ``export_all_blueprint_rules``, the full pipeline for writing
blueprints as Continue AI rule files via ``RuleFile``
"""

from pathlib import Path

from kaye import logger
from kaye.prompt import load_prompt_corpus_tree
from kaye.prompt.prompt_blueprint import PromptBlueprint

from kaye.cli import EXPORTABLE_BLUEPRINTS
from kaye.cli.cli_continue.rule_file import RuleFile

# constants  ###################################################################


_ALWAYS_APPLY_BLUEPRINT = [
    "Chat",
    "Coder",
    "Agent Behavior",
    "Continue Behavior",
]


_continue_behavior_blueprint = PromptBlueprint.create_from_node(
    load_prompt_corpus_tree()["Agent Behavior"]["Continue Behavior"]
)


# Entry Point  #################################################################
def export_blueprint_rules(rules_folder):
    """
    export all blueprints in ``EXPORT_BLUEPRINTS`` as Continue AI rule files

    creates ``rules_folder`` if it does not exist, then calls
    ``export_blueprint_rule`` for each listed blueprint

    :param rules_folder: destination folder for rule files
    :type rules_folder: Path-like
    """
    folder_path = Path(rules_folder).resolve()
    folder_path.mkdir(parents=True, exist_ok=True)

    for bp in EXPORTABLE_BLUEPRINTS + [_continue_behavior_blueprint]:
        name = bp.display_name
        file_path = folder_path / "{}.md".format(bp.display_name)

        with RuleFile(file_path, blueprint=bp) as rule:
            rule.always_apply = name in _ALWAYS_APPLY_BLUEPRINT

        logger.succ("blueprint rule:\t{}".format(file_path))
