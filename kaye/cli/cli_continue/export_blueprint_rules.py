"""
blueprint_rule.py

define ``export_all_blueprint_rules``, the full pipeline for writing
blueprints as Continue AI rule files via ``RuleFile``
"""

from pathlib import Path

from kaye.prompt import load_prompt_corpus_tree
from kaye.prompt.prompt_blueprint import PromptBlueprint

from kaye.cli import EXPORTABLE_BLUEPRINTS
from kaye.cli.cli_continue.rule_file import RuleFile

# constants  ###################################################################

# Todo globs saved in corpus
_BLUEPRINT_NAME2GLOBS = {
    "Coder C": ["**/*.{c,h}"],
    "Coder CPP": ["**/*.{cpp,cc,cxx,hpp,hh,hxx}"],
    "Coder Unreal Engine": ["**/*.{cpp,cc,cxx,hpp,hh,hxx}"],
    "Coder C Sharp": ["**/*.cs"],
    "Coder Unity Engine": ["**/*.cs"],
    "Coder GDScript": ["**/*.gd"],
    "Coder HTML": ["**/*.{html,htm}"],
    "Coder JavaScript and TypeScript": ["**/*.{js,ts,jsx,tsx,mjs,cjs}"],
    "Coder Python": ["**/*.py"],
    "Coder Python Docstring Style": ["**/*.py"],
    "Coder Python Testing Guidelines": ["**/test_*.py", "**/*_test.py"],
    "Project CHANGELOG Writer": [
        "**/{CHANGELOG,Changelog,changelog}{,.md,.txt}",
    ],
    "Project AGENTS Writer": [
        "**/{AGENTS,Agents,agents}{,.md}",
    ],
    "Project README Writer": [
        "**/{README,Readme,readme}{,.md,.txt}",
    ],
}

_ALWAYS_APPLY_BLUEPRINT = [
    "Chat",
    "Coder",
    "Agent Behavior",
    "Continue Behavior",
]


_continue_behavior_blueprint = PromptBlueprint.create_from_node(
    load_prompt_corpus_tree()["Continue Behavior"]
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
            rule.globs = _BLUEPRINT_NAME2GLOBS.get(name, [])
            rule.always_apply = name in _ALWAYS_APPLY_BLUEPRINT

        print("update blueprint rule:\t{}".format(file_path))
