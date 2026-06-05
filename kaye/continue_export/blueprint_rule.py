"""
blueprint_rule.py

define ``export_all_blueprint_rules``, the full pipeline for writing
blueprints as Continue AI rule files via ``RuleFile``
"""

from pathlib import Path

from kaye.continue_export.rule_file import RuleFile
from kaye.prompt import embedded_blueprints
from kaye.prompt.prompt_blueprint import PromptBlueprint

# constants  ###################################################################

_CODER_BLUEPRINT_GLOBS = {
    "coder_c_blueprint": ["**/*.{c,h}"],
    "coder_cpp_blueprint": ["**/*.{cpp,cc,cxx,hpp,hh,hxx}"],
    "coder_ue_blueprint": ["**/*.{cpp,cc,cxx,hpp,hh,hxx}"],
    "coder_csharp_blueprint": ["**/*.cs"],
    "coder_u3d_blueprint": ["**/*.cs"],
    "coder_gdscript_blueprint": ["**/*.gd"],
    "coder_html_blueprint": ["**/*.{html,htm}"],
    "coder_js_ts_blueprint": ["**/*.{js,ts,jsx,tsx,mjs,cjs}"],
    "coder_py_blueprint": ["**/*.py"],
    "coder_py_docstring_blueprint": ["**/*.py"],
    "coder_py_testing_blueprint": ["**/test_*.py", "**/*_test.py"],
    "coder_changelog_blueprint": [
        "**/{CHANGELOG,Changelog,changelog}{,.md,.txt}",
    ],
}

_ALWAYS_APPLY_BLUEPRINT = [
    "chat_blueprint",
    "coder_blueprint",
    "continue_behavior_blueprint",
]

_EXPORT_BLUEPRINTS = [
    "chat_blueprint",
    "date_time_blueprint",
    "number_unit_blueprint",
    "style_blueprint",
    "annotation_marker_blueprint",
    "coder_blueprint",
    "coder_changelog_blueprint",
    "coder_project_blueprint",
    "coder_bash_blueprint",
    "coder_c_blueprint",
    "coder_cpp_blueprint",
    "coder_ue_blueprint",
    "coder_csharp_blueprint",
    "coder_u3d_blueprint",
    "coder_gdscript_blueprint",
    "coder_html_blueprint",
    "coder_js_ts_blueprint",
    "coder_py_blueprint",
    "coder_py_docstring_blueprint",
    "coder_py_testing_blueprint",
    "continue_behavior_blueprint",
]


# helpers  #####################################################################


def _export_blueprint_rule(name, bp, path):
    """
    write a single blueprint as a Continue AI rule file

    resolves globs and always-apply status from ``name``, then
    delegates all file writing to ``RuleFile``

    :param name: blueprint registry name, used to look up globs
            and always-apply status
    :type name: str
    :param bp: blueprint object exposing ``display_name``,
            ``description``, and ``generate_prompt()``
    :param path: destination path for the rule file
    :type path: Path-like
    """
    with RuleFile(path, encoding="utf-8") as rule:
        rule.name = bp.display_name
        rule.description = bp.description
        rule.globs = _CODER_BLUEPRINT_GLOBS.get(name, [])
        rule.always_apply = name in _ALWAYS_APPLY_BLUEPRINT
        rule.write_prefix()
        rule.write(bp.generate_prompt())


# continue behavior blueprint  ------------------------------------------------

_continue_behavior_blueprint = PromptBlueprint.create_empty_blueprint()
_continue_behavior_blueprint.checkmark(
    _continue_behavior_blueprint.corpus["Continue"]["Continue Behavior"]
)
_continue_behavior_blueprint.display_name = "Continue Behavior"


# Entry Point  #################################################################
def export_blueprint_rules(rules_folder):
    """
    export all blueprints in ``EXPORT_BLUEPRINTS`` as Continue AI rule files

    creates ``rules_folder`` if it does not exist, then calls
    ``export_blueprint_rule`` for each listed blueprint

    :param rules_folder: destination folder for rule files
    :type rules_folder: Path-like
    """
    folder = Path(rules_folder).resolve()
    folder.mkdir(parents=True, exist_ok=True)

    _local = {
        "continue_behavior_blueprint": _continue_behavior_blueprint,
    }

    for name in _EXPORT_BLUEPRINTS:
        bp = _local.get(name) or getattr(embedded_blueprints, name)
        file_path = folder / "{}.md".format(name)

        print("update blueprint rule:\t{}".format(file_path))
        _export_blueprint_rule(name, bp, file_path)
