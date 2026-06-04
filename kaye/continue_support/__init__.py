"""
define ``update_continue_local_config_folder``
"""

from pathlib import Path


def update_continue_local_config_folder(continue_local_config_folder):
    """
    HACK HACK write docstring


    :param continue_local_config_folder: path to folder containing
            continue local configs,
            i.e. the ``.continue/`` folder containing
            ``config.yaml``, ``sessions/``, ``rules/``
    :type continue_local_config_folder: Path-like
    """
    folder = Path(continue_local_config_folder)
    rules_folder = (folder / "rules").resolve()

    print(rules_folder)  # HACK


class RuleFile:

    def __init__(self, path, mode="w", encoding=None):
        self._path = path
        self._mode = mode
        self._encoding = encoding

        self.name = ""
        self.description = ""
        self.globs = ""
        self.always_apply = ""

        self.f = None

    def __enter__(self):
        self.f = open(self._path, self._mode, encoding=self._encoding)
        return self

    def __exit__(self, *args):
        self.f.close()

    def write_prefix(self):
        self.f.write("---\n")
        self.f.write("name: {}\n".format(self.name))

        if self.description:
            self.f.write("description: {}\n".format(self.description))

        if self.globs:
            self.f.write("globs: {}\n".format(self.globs))

        if self.always_apply:
            self.f.write("alwaysApply: {}\n".format(self.always_apply))

        self.f.write("---\n\n")
