"""
define ``update_continue_local_config_folder``
"""

from pathlib import Path


def update_continue_local_config_folder(continue_local_config_folder):
    """
    HACK write docstring


    :param continue_local_config_folder: path to folder containing
            continue local configs,
            i.e. the ``.continue/`` folder containing
            ``config.yaml``, ``sessions/``, ``rules/``
    :type continue_local_config_folder: Path-like
    """
    folder = Path(continue_local_config_folder)
    rules_folder = (folder / "rules").resolve()

    pass  # TODO


class RuleFile:

    def __init__(self, path, is_invokable, mode="w", encoding=None):
        self._is_invokable = is_invokable
        self._path = path
        self._mode = mode
        self._encoding = encoding

        self._file = None

    def __enter__(self):
        self._file = open(self._path, self._mode, encoding=self._encoding)
        return self

    def __exit__(self, *args):
        self._file.close()

    def write(self, name, content):
        f = self._file

        f.write("---")
        f.write("name: {}".format(name))
        if self._is_invokable:
            f.write("invokable: true")
        f.write("---")

        f.write(content)
