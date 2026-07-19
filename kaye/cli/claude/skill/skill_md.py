"""
skill_md_file.py

define ``SkillMDFile``
"""

import io
from importlib.metadata import version

import yaml

from kaye import PROGRAM_NAME
from kaye.cli.claude import (
    convert_display_name2skill_name,
    CONTAINING_SIDECAR_NODES,
)
from kaye.cli.frontmatter_md_file import FrontmatterMDFile


class SkillMDFile(FrontmatterMDFile):  #########################################
    """
    manage metadata and content writing for an agent skill markdown file


    :param folder_path: folder to write SKILL.md into
    :type folder_path: Path-like
    :param registry: blueprint registry entry
    :type registry: BlueprintRegistry
    :example:
    >>> # blueprint-based skills
    ... with SkillMDFile(parent_folder, registry=reg) as skill:
    ...     pass

    >>> # abbreviation skills
    ... with SkillMDFile(parent_folder) as skill:
    ...     skill.name = ~~
    ...     skill.description = ~~
    ...     skill.write_frontmatter_part()
    ...     skill.write(~~)
    ...     ~~
    """

    # implement FrontmatterMDFile  =============================================

    def _write_frontmatter_content(self):
        d = {
            key: value
            for key, value in self.frontmatter.items()
            if value != self._DEFAULT_FRONTMATTER.get(key)
        }

        yaml_buffer = io.StringIO()
        yaml.dump(
            d,
            yaml_buffer,
            default_flow_style=False,
            sort_keys=False,
            width=float("inf"),
        )
        self.file.write(yaml_buffer.getvalue())

    # constants  ===============================================================

    _DEFAULT_FRONTMATTER = {
        "name": "",
        "description": "",
        "when_to_use": "",
        "license": "",
        "compatibility": "",
        "metadata": {},
        "allowed-tools": [],
        "user-invocable": True,
        "paths": [],
    }

    _FILENAME = "SKILL.md"

    def __init__(self, folder_path, *, registry=None):
        file_name = folder_path / self._FILENAME
        super().__init__(
            file_name,
            registry,
            contains_sidecar_nodes=CONTAINING_SIDECAR_NODES,
        )

        self.frontmatter["metadata"]["version"] = version(PROGRAM_NAME)

        if registry:
            self.name = convert_display_name2skill_name(registry.display_name)
            globs = registry.blueprint.sidecars.globs
            if globs:
                self.frontmatter["paths"] = list(globs)
