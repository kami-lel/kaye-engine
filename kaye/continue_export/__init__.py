"""
continue_export

export Kaye prompts and blueprints as Continue AI rule files (``.mdc``).

defines blueprint glob patterns and always-apply lists used when
writing rule files to a Continue local config folder.
"""

from kaye.continue_export.blueprint_rule import export_all_blueprint_rules
from kaye.continue_export.rule_file import RuleFile

__all__ = [
    "RuleFile",
    "export_all_blueprint_rules",
]

# todo continue support *prompts*
# TODO abbreviations
