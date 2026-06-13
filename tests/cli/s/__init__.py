from pydantic import BaseModel, Field

from kaye.cli.cli_skill import convert_display_name2skill_name

# TODO content test
# FIXME move below class down one level


class SkillMDFileFrontmatterValidator(BaseModel):
    """
    validated frontmatter model for an agent skill SKILL.md file


    required fields: ``name``, ``description``
    optional fields omitted from output when empty: ``license``,
    ``compatibility``, ``metadata``, ``allowed_tools``
    """

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


# helpers  #####################################################################


def _validate_exportable(obj):
    return SkillMDFileFrontmatterValidator.from_frontmatter({
        "name": convert_display_name2skill_name(obj.display_name),
        "description": obj.description,
    })


validate_blueprint = _validate_exportable
validate_abbr_group = _validate_exportable
