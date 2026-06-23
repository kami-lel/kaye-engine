from pydantic import BaseModel, Field

from kaye.cli.cli_claude import convert_display_name2skill_name

# FIXME FIXME move validator to corpus test


class SkillMDFileFrontmatterValidator(BaseModel):
    """
    validated frontmatter model for an agent skill SKILL.md file


    required fields: ``name``
    optional fields omitted from output when empty: ``description``,
    ``license``, ``compatibility``, ``metadata``, ``allowed_tools``,
    ``user_invocable``, ``when_to_use``, ``paths``
    """

    # required  ================================================================

    name: str = Field(
        min_length=1,
        max_length=64,
        pattern=r"^[a-z0-9]([a-z0-9]|-[a-z0-9])*$",
    )

    # optional  ================================================================

    description: str | None = Field(None, max_length=1024)
    license: str | None = None
    compatibility: str | None = Field(None, max_length=500)
    metadata: dict | None = None
    allowed_tools: str | None = Field(None, alias="allowed-tools")
    user_invocable: bool | None = Field(None, alias="user-invocable")
    when_to_use: str | None = None
    paths: list[str] | None = None

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


# helpers  #####################################################################


def validate_blueprint(obj):
    return SkillMDFileFrontmatterValidator.from_frontmatter({
        "name": convert_display_name2skill_name(obj.display_name),
        "description": obj.meta.description or None,
    })


def validate_abbr_group(obj):
    return SkillMDFileFrontmatterValidator.from_frontmatter({
        "name": convert_display_name2skill_name(obj.display_name),
        "description": obj.description or None,
    })
