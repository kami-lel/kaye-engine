"""
rule_file.py

define ``RuleFile``
"""

import io
import yaml

from kaye.cli.frontmatter_md_file import FrontmatterMDFile


class RuleFile(FrontmatterMDFile):  ############################################
    """
    manage metadata and content writing for a Continue AI rule file


    :param path:
    :type path: Path-like
    :param blueprint: optional blueprint object
    :type blueprint: PromptBlueprint or None
    :example:
    >>> # blueprint rule file
    >>> with RuleFile(path, blueprint=bp) as rule:
    ...     rule.globs = ["**/*.py"]
    ...     rule.always_apply = False

    >>> # abbreviation rule file
    >>> with RuleFile(path) as rule:
    ...     rule.name = "Abbr Prefixes"
    ...     rule.write_frontmatter()
    ...     rule.write(entries)
    """

    # implement FrontmatterMDFile  =============================================

    def write_frontmatter(self):
        self.file.write("---\n")

        metadata = {"name": self.frontmatter.get("name", "")}

        description = self.frontmatter.get("description", "")
        if description:
            metadata["description"] = description

        metadata["alwaysApply"] = self.always_apply

        if self.invokable:
            metadata["invokable"] = self.invokable

        yaml_buffer = io.StringIO()
        yaml.dump(
            metadata,
            yaml_buffer,
            default_flow_style=False,
            sort_keys=False,
            width=float("inf"),
        )
        self.file.write(yaml_buffer.getvalue())

        if self.globs:
            globs_str = ", ".join('"{}"'.format(g) for g in self.globs)
            self.file.write("globs: [{}]\n".format(globs_str))

        self.file.write("---\n\n")

    # constructor  =============================================================

    def __init__(self, path, blueprint=None):
        super().__init__(path, blueprint)

        self.globs = []
        self.always_apply = False
        self.invokable = False
