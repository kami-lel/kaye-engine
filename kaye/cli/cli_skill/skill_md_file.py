"""
skill_md_file.py

define ``SkillMDFile``
"""

import io

import yaml
from pydantic import BaseModel, Field

from kaye.cli.frontmatter_md_file import FrontmatterMDFile

# helper  ######################################################################


class _SkillFrontmatter(BaseModel):  ###########################################
    """
    validated frontmatter model for an agent skill SKILL.md file


    required fields: ``name``, ``description``
    optional fields omitted from output when empty: ``license``,
    ``compatibility``, ``metadata``, ``allowed_tools``
    """

    # fields  ==================================================================

    model_config = {"populate_by_name": True}

    # required

    name: str = Field(
        min_length=1,
        max_length=64,
        pattern=r"^[a-z0-9]([a-z0-9]|-[a-z0-9])*$",
    )
    description: str = Field(min_length=1, max_length=1024)

    # optional

    license: str | None = None
    compatibility: str | None = Field(None, max_length=500)
    metadata: dict | None = None
    allowed_tools: str | None = Field(None, alias="allowed-tools")

    # serialization  ===========================================================

    @classmethod
    def from_frontmatter(cls, d: dict):
        """construct and validate from a ``FrontmatterMDFile.frontmatter`` dict"""
        allowed = d.get("allowed-tools")
        if isinstance(allowed, list):
            allowed = " ".join(allowed) if allowed else None

        return cls.model_validate({
            "name": d.get("name", ""),
            "description": d.get("description", ""),
            "license": d.get("license") or None,
            "compatibility": d.get("compatibility") or None,
            "metadata": d.get("metadata") or None,
            "allowed-tools": allowed,
        })

    def to_dict(self) -> dict:
        """ordered dict for YAML output; optional fields omitted when empty"""
        d = {"name": self.name, "description": self.description}
        if self.license:
            d["license"] = self.license
        if self.compatibility:
            d["compatibility"] = self.compatibility
        if self.metadata:
            d["metadata"] = self.metadata
        if self.allowed_tools:
            d["allowed-tools"] = self.allowed_tools
        return d


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
        validated = _SkillFrontmatter.from_frontmatter(self.frontmatter)

        yaml_buffer = io.StringIO()
        yaml.dump(
            validated.to_dict(),
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
