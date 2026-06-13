"""
skill_md_file.py

define ``SkillMDFile``
"""

import io
from importlib.metadata import version

import yaml

from kaye.cli.cli_skill import convert_display_name2skill_name
from kaye.cli.frontmatter_md_file import FrontmatterMDFile


class SkillMDFile(FrontmatterMDFile):  #########################################
    """
    manage metadata and content writing for an agent skill markdown file


    :param folder_path: folder to write SKILL.md into
    :type folder_path: Path-like
    :param blueprint: blueprint object
    :type blueprint: PromptBlueprint
    :example:
    >>> # blueprint-based skills
    ... with SkillMDFile(parent_folder, blueprint=bp) as skill:
    ...     pass

    >>> # abbreviation skills
    ... with SkillMDFile(parent_folder, blueprint=bp) as skill:
    ...     skill.name = ~~
    ...     skill.description = ~~
    ...     skill.write_frontmatter_part()
    ...     skill.write(~~)
    ...     skill.writelines(~~)
    ...     ~~
    """

    # implement FrontmatterMDFile  =============================================

    def _write_frontmatter_content(self):
        d = {
            "name": self.frontmatter["name"],
            "description": self.frontmatter["description"],
        }

        for key in ("license", "compatibility", "metadata", "allowed-tools"):
            value = self.frontmatter.get(key)
            if value:
                d[key] = value

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

    _FILENAME = "SKILL.md"

    def __init__(self, folder_path, *, blueprint=None, includes_version=False):
        file_name = folder_path / self._FILENAME
        super().__init__(file_name, blueprint)

        if includes_version:
            self.frontmatter["metadata"]["version"] = version("kaye")

        if blueprint:
            self.name = convert_display_name2skill_name(blueprint.display_name)
