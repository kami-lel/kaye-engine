"""
define ``update_continue_local_config_folder``
"""

from pathlib import Path

from kaye.prompt import embedded_blueprints
from kaye.prompt.embedded_blueprints import __all__ as BLUEPRINT_NAMES
from kaye.continue_support.rule_file import RuleFile


def update_continue_local_config_folder(continue_local_config_folder):
    """
    update the Continue local config folder with the updated kaye prompts


    :param continue_local_config_folder: path to folder containing
            continue local configs,
            i.e. the ``.continue/`` folder containing
            ``config.yaml``, ``sessions/``, ``rules/``, etc.
    :type continue_local_config_folder: Path-like
    """
    folder = Path(continue_local_config_folder)
    rules_folder = (folder / "rules").resolve()
    rules_folder.mkdir(parents=True, exist_ok=True)

    for name in BLUEPRINT_NAMES:
        bp = getattr(embedded_blueprints, name)
        file_path = rules_folder / "{}.md".format(name)

        print("update rule: {}".format(file_path))
        with RuleFile(file_path, encoding="utf-8") as rule:
            rule.name = bp.display_name
            rule.description = bp.description
            rule.write_prefix()
            rule.write(bp.generate_prompt())
            # TODO glob

    # todo support *prompts*
