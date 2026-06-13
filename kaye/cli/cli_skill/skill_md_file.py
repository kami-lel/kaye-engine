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
    :example:
    >>> with SkillMDFile(folder) as md_file:
    ...     md_file.blueprint = blueprint
    ...     md_file.version = "v1.0.0"
    """

    # implement FrontmatterMDFile  =============================================

    def write_frontmatter(self):
        self.file.write("---\n")

        yaml_buffer = io.StringIO()
        yaml.dump(
            self.frontmatter,
            yaml_buffer,
            default_flow_style=False,
            sort_keys=False,
            width=float("inf"),
        )
        self.file.write(yaml_buffer.getvalue())

        self.file.write("---\n\n")

    # constants  ===============================================================

    _FILENAME = "SKILL.md"

    def __init__(self, folder_path):
        file_name = folder_path / self._FILENAME
        super().__init__(file_name)
