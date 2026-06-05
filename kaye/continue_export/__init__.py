"""
continue_export

export Kaye prompts and blueprints as Continue AI rule files (``.mdc``).

defines blueprint glob patterns and always-apply lists used when
writing rule files to a Continue local config folder.
"""

from kaye.continue_export.blueprint_rule import (
    ALWAYS_APPLY_BLUEPRINT,
    CODER_BLUEPRINT_GLOBS,
    EXPORT_BLUEPRINTS,
    export_all_blueprint_rules,
    export_blueprint_rule,
)
from kaye.continue_export.rule_file import RuleFile

__all__ = [
    "RuleFile",
    "export_blueprint_rule",
    "export_all_blueprint_rules",
    "CODER_BLUEPRINT_GLOBS",
    "ALWAYS_APPLY_BLUEPRINT",
    "EXPORT_BLUEPRINTS",
]

# TODO continue support *prompts*
# TODO abbreviations
# TODO add blueprint rule file
