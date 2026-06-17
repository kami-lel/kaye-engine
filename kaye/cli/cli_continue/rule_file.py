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
    ... with RuleFile(path, blueprint=bp) as rule:
    ...     rule.always_apply = False

    >>> # abbreviation rule file
    ... with RuleFile(path) as rule:
    ...     rule.name = ~~
    ...     rule.description = ~~
    ...     rule.write_frontmatter_part()
    ...     rule.write(~~)
    ...     ~~
    """

    # implement FrontmatterMDFile  =============================================

    def _write_frontmatter_content(self):
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

        globs = self.frontmatter["globs"]
        if globs:
            globs_str = ", ".join('"{}"'.format(g) for g in globs)
            self.file.write("globs: [{}]\n".format(globs_str))

    # constructor  =============================================================

    def __init__(self, path, blueprint=None):
        super().__init__(path, blueprint)

        self.always_apply = False
        self.invokable = False

        if blueprint:
            self.name = blueprint.display_name
            self.description = blueprint.meta.description_and_when_to_use
            self.frontmatter["globs"] = blueprint.meta.globs
