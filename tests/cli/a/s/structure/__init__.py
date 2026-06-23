from kaye.cli.cli_claude import convert_display_name2skill_name

from tests.corpus import SkillMDFileFrontmatterValidator


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
