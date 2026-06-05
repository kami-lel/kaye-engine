"""
continue_support.py

define ``RuleFile`` and ``update_continue_local_config_folder``
"""

from pathlib import Path

from kaye.prompt import embedded_blueprints
from kaye.prompt.embedded_blueprints import __all__ as BLUEPRINT_NAMES

# todo continue support *prompts*
# Fixme split as package
# Todo abbreviations
# Todo add blueprint rule file


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


# RuleFile  ####################################################################


class RuleFile:
    """
    context manager for writing a Continue AI rule file (``.mdc``)

    :param path: path to the rule file to write
    :type path: Path-like
    :param mode: file open mode, defaults to ``"w"``
    :type mode: str, optional
    :param encoding: file encoding, defaults to None
    :type encoding: str, optional
    :example:
    >>> with RuleFile("my-rule.mdc") as rule:
    ...     rule.name = "My Rule"
    ...     rule.description = "does something useful"
    ...     rule.globs = ["**/*.py"]
    ...     rule.write_prefix()
    ...     rule.write("always do this\n")
    """

    def __init__(self, path, mode="w", encoding=None):
        self._path = path
        self._mode = mode
        self._encoding = encoding

        self.name = ""
        self.description = ""
        self.globs = []
        self.always_apply = False

        self.file = None

    def __enter__(self):
        self.file = open(self._path, self._mode, encoding=self._encoding)
        return self

    def __exit__(self, *args):
        self.file.close()

    def write_prefix(self):
        """
        write the YAML front matter block using the current attribute values
        """
        self.file.write("---\n")
        self.file.write("name: {}\n".format(self.name))

        if self.description:
            self.file.write("description: {}\n".format(self.description))

        if self.globs:
            globs_str = ", ".join('"{}"'.format(g) for g in self.globs)
            self.file.write("globs: [{}]\n".format(globs_str))

        self.file.write(
            "alwaysApply: {}\n".format(str(self.always_apply).lower())
        )

        self.file.write("---\n\n")

    def write(self, content):
        """
        write ``content`` directly to the rule file

        :param content: text to write
        :type content: str
        """
        self.file.write(content)


# Entry Point  #################################################################


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
            rule.globs = CODER_BLUEPRINT_GLOBS.get(name, [])
            rule.always_apply = name in ALWAYS_APPLY_BLUEPRINT
            rule.write_prefix()
            rule.write(bp.generate_prompt())
