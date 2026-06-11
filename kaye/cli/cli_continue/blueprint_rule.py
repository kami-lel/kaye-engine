"""
blueprint_rule.py

define ``export_all_blueprint_rules``, the full pipeline for writing
blueprints as Continue AI rule files via ``RuleFile``
"""

from pathlib import Path

from kaye.prompt import embedded_blueprints
from kaye.prompt.prompt_blueprint import PromptBlueprint

from kaye.cli.cli_continue.rule_file import RuleFile

# constants  ###################################################################

_BLUEPRINT_NAME2GLOBS = {
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
    "project_changelog_blueprint": [
        "**/{CHANGELOG,Changelog,changelog}{,.md,.txt}",
    ],
    "project_agents_blueprint": [
        "**/{AGENTS,Agents,agents}{,.md}",
    ],
    "project_readme_blueprint": [
        "**/{README,Readme,readme}{,.md,.txt}",
    ],
}

_ALWAYS_APPLY_BLUEPRINT = [
    "chat_blueprint",
    "coder_blueprint",
    "continue_behavior_blueprint",
]

_OLD_EXPORT_BLUEPRINTS = [
    "date_time_blueprint",
    "number_unit_blueprint",
    "annotation_marker_blueprint",
    "coder_blueprint",
    "project_structure_blueprint",
    "project_readme_blueprint",
    "project_changelog_blueprint",
    "project_agents_blueprint",
    "project_semantic_versioning_blueprint",
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
    "style_capitalization_blueprint",
    "style_briefness_blueprint",
    "style_good_writing_blueprint",
]

_EXPORT_BLUEPRINTS = [
    "chat_blueprint",
    "style_capitalization_blueprint",
    "style_briefness_blueprint",
    "style_good_writing_blueprint",
]


# continue behavior blueprint  ------------------------------------------------

_continue_behavior_blueprint = PromptBlueprint.create_empty_blueprint()
_continue_behavior_blueprint.checkmark(
    _continue_behavior_blueprint.corpus["Continue"]["Continue Behavior"]
)
_continue_behavior_blueprint.display_name = "Continue Behavior"

_local_bp = {
    "continue_behavior_blueprint": _continue_behavior_blueprint,
}


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

    # FIXME FIXME remove
    for bp_id in _OLD_EXPORT_BLUEPRINTS:
        bp = _local_bp.get(bp_id) or getattr(embedded_blueprints, bp_id)
        file_path = folder_path / "{}.md".format(bp.display_name)

        print("update blueprint rule:\t{}".format(file_path))

        with RuleFile(file_path, blueprint=bp) as rule:
            rule.globs = _BLUEPRINT_NAME2GLOBS.get(bp_id, [])
            rule.always_apply = bp_id in _ALWAYS_APPLY_BLUEPRINT
            rule.write_frontmatter_and_content()

    for bp_id in _EXPORT_BLUEPRINTS:
        bp = _local_bp.get(bp_id) or getattr(embedded_blueprints, bp_id)
        file_path = folder_path / "{}.md".format(bp.display_name)

        with RuleFile(file_path, blueprint=bp) as rule:
            rule.globs = _BLUEPRINT_NAME2GLOBS.get(bp_id, [])
            rule.always_apply = bp_id in _ALWAYS_APPLY_BLUEPRINT
            rule.write_frontmatter_and_content()

        print("update blueprint rule:\t{}".format(file_path))
