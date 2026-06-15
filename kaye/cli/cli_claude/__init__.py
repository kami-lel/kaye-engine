"""
CLI subcommand for Anthropic Claude Skill & Plugin integration.
"""


def convert_display_name2skill_name(display_name):
    """
    convert a blueprint display name to a kebab-case skill name


    :param display_name: human-readable blueprint display name
    :type display_name: str
    :returns: lowercase, hyphen-separated skill name
    :rtype: str
    """
    return display_name.replace(" ", "-").lower()


# Todo write unit tests for all cases

# TODO use kamilog in claude
# FIXME use newer version
