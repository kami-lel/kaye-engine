from pydantic import BaseModel, Field

from kaye.cli.cli_skill import convert_display_name2skill_name


# TODO TODO unit tests on skill rule
class SkillMDFileFrontmatterValidator(BaseModel):
    """
    validated frontmatter model for an agent skill SKILL.md file


    required fields: ``name``, ``description``
    optional fields omitted from output when empty: ``license``,
    ``compatibility``, ``metadata``, ``allowed_tools``
    """

    model_config = {"populate_by_name": True}

    # required  ================================================================

    name: str = Field(
        min_length=1,
        max_length=64,
        pattern=r"^[a-z0-9]([a-z0-9]|-[a-z0-9])*$",
    )
    description: str = Field(min_length=1, max_length=1024)

    # optional  ================================================================

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


# helpers  #####################################################################


def validate_blueprint(bp):
    """Validate frontmatter derived from a PromptBlueprint."""
    return SkillMDFileFrontmatterValidator.from_frontmatter({
        "name": convert_display_name2skill_name(bp.display_name),
        "description": bp.description,
    })


def validate_abbr_group(group):
    """Validate frontmatter derived from an ExportableAbbr group."""
    return SkillMDFileFrontmatterValidator.from_frontmatter({
        "name": convert_display_name2skill_name(group.display_name),
        "description": group.description,
    })
