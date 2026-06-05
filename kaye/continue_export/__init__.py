"""
continue_export

export Kaye prompts and blueprints as Continue AI rule files (``.mdc``).

defines blueprint glob patterns and always-apply lists used when
writing rule files to a Continue local config folder.
"""

from kaye.continue_export.rule_file import RuleFile

__all__ = ["RuleFile", "CODER_BLUEPRINT_GLOBS", "ALWAYS_APPLY_BLUEPRINT"]

# TODO continue support *prompts*
# TODO abbreviations
# TODO add blueprint rule file


# constants  ###################################################################

CODER_BLUEPRINT_GLOBS = {
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

ALWAYS_APPLY_BLUEPRINT = [
    "chat_blueprint",
    "coder_blueprint",
    "continue_behavior_blueprint",
]
