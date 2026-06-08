"""
rule_file.py

define ``RuleFile``, a context manager for writing Continue AI rule files
"""


class RuleFile:
    """
    context manager for writing a Continue AI rule file (``.mdc``)

    :param path: path to the rule file to write
    :type path: Path-like
    :param mode: file open mode, defaults to ``"w"``
    :type mode: str, optional
    :param encoding: file encoding, defaults to ``None``
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
        self.invokable = False

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

        if self.invokable:
            self.file.write("invokable: true\n")

        self.file.write("---\n\n")

    def write(self, content):
        """
        write ``content`` directly to the rule file

        :param content: text to write
        :type content: str
        """
        self.file.write(content)
