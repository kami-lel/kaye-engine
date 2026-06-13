"""
skill_md_file.py

define ``SkillMDFile``
"""

import io

import yaml

from kaye.cli.frontmatter_md_file import FrontmatterMDFile


class SkillMDFile(FrontmatterMDFile):  #########################################
    """
    manage metadata and content writing for an agent skill markdown file


    :param folder_path: folder to write SKILL.md into
    :type folder_path: Path-like
    :param blueprint: blueprint object
    :type blueprint: PromptBlueprint
    :example:
    >>> with SkillMDFile(folder, blueprint) as md_file:
    ...     md_file.version = "v1.0.0"
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

    def __init__(self, folder_path, blueprint=None):
        file_name = folder_path / self._FILENAME
        super().__init__(file_name, blueprint)

        if blueprint:
            self.name = blueprint.skill_name
