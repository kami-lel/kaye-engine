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
    :param registry: optional blueprint registry entry; ``always_apply`` and
            ``invokable`` are taken from it directly
    :type registry: BlueprintRegistry or None
    :example:
    >>> # blueprint rule file
    ... with RuleFile(path, registry=reg) as rule:
    ...     pass

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

    def __init__(self, path, registry=None):
        super().__init__(path, registry)

        self.always_apply = False
        self.invokable = False

        if registry:
            self.name = registry.display_name
            self.description = (
                registry.blueprint.sidecars.description_and_when_to_use
            )
            self.frontmatter["globs"] = registry.blueprint.sidecars.globs
            self.always_apply = registry.always_apply
            self.invokable = registry.invokable
