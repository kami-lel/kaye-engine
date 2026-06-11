"""
skill_md_file.py

define ``SkillMDFile``
"""

import io
import yaml


class SkillMDFile:  ############################################################
    """
    manage metadata and content writing for an agent skill markdown file


    :param path:
    :type path: Path-like
    :param blueprint: blueprint object
    :type blueprint: PromptBlueprint
    :example:
    >>> with SkillMDFile("my_skill.md", blueprint) as md_file:
    ...     md_file.version = "v1.0.0"
    ...     md_file.write_frontmatter()
    ...     md_file.write_content()
    """

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

    def write_content(self):
        self.file.write(self._blueprint.generate_prompt())

    # properties  ==============================================================

    def _set_version(self, value):
        self.frontmatter.setdefault("metadata", {})["version"] = value

    version = property(fset=_set_version)

    # constants  ===============================================================

    _FILE_MODE = "w"
    _FILE_ENCODING = "utf-8"
    _FILENAME = "SKILL.md"

    def __init__(self, folder_path, blueprint):
        self._folder_path = folder_path
        self._blueprint = blueprint

        self.file = None

        # frontmatter  ---------------------------------------------------------
        self.frontmatter = {
            "name": blueprint.display_name if blueprint else "",
            "description": blueprint.description if blueprint else "",
            "license": "",
            "compatibility": "",
            "metadata": {},
            "allowed-tools": [],
        }

    # support context manager  =================================================

    def __enter__(self):
        self.file = open(
            self._folder_path / self._FILENAME,
            self._FILE_MODE,
            encoding=self._FILE_ENCODING,
        )
        return self

    def __exit__(self, *_):
        self.file.close()

    # TODO version auto read
