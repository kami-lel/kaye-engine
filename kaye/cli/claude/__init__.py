"""
CLI subcommand for Anthropic Claude Skill & Plugin integration.
"""

import re

from kaye.prompt.meta_node_type import MetaNodeType

# meta node types to auto-checkmark when exporting Claude prompts
CONTAINING_META_NODES = MetaNodeType.FOR_CLAUDE | MetaNodeType.PREREQUISITE


def convert_display_name2skill_name(display_name):
    """
    convert a blueprint display name to a kebab-case skill name

    the result matches Anthropic's skill-name grammar
    ``^[a-z0-9]([a-z0-9]|-[a-z0-9])*$``: every run of characters outside
    ``[a-z0-9]`` collapses to a single hyphen and leading/trailing hyphens
    are stripped, so a name such as ``Abbr Starts with Digits 0~9`` yields
    ``abbr-starts-with-digits-0-9`` rather than an upload-rejected slug
    containing ``~``


    :param display_name: human-readable blueprint display name
    :type display_name: str
    :returns: lowercase, hyphen-separated skill name
    :rtype: str
    """
    return re.sub(r"[^a-z0-9]+", "-", display_name.lower()).strip("-")
