"""
emoji_node.py

define the emoji-tagged abbr node type
"""

from kaye_engine.abbr_collection import AbbrTags
from kaye_engine.prompt.dynamic_nodes.shorthand_tag_nodes import (
    gen_shorthand_content_lines,
)
from .dynamic_node import DynamicNode

__all__ = ("EmojiNode",)


class EmojiNode(DynamicNode):  ##################################################
    """
    dynamic node to provide every abbr entry tagged ``emoji``
    """

    # implement DynamicNode  ===================================================

    HEADING = "Emoji"

    # implement BasePromptNode  ================================================

    def content_lines(self, **kwargs):  # pylint: disable=unused-argument
        return self._preface + gen_shorthand_content_lines(AbbrTags.emoji)
