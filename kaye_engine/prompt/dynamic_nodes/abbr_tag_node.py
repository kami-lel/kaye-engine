"""
abbr_tag_node.py

define ``AbbrTagNode``, ``ABBR_TAG_NODE_MEMBERS``, and
``heading_for_abbr_tag``
"""

from kaye_engine.abbr_collection import AbbrTags
from kaye_engine.prompt.dynamic_nodes.shorthand_tag_nodes import (
    gen_shorthand_content_lines,
)
from .dynamic_node import DynamicNode

__all__ = ("AbbrTagNode", "ABBR_TAG_NODE_MEMBERS", "heading_for_abbr_tag")

# excluded from ABBR_TAG_NODE_MEMBERS: already covered by ShorthandNode's
# no-query fallback
_EXCLUDED_ABBR_TAGS = frozenset({AbbrTags.always_understand})

# every simple (single-bit) AbbrTags member eligible for its own node --
# composite members (e.g. WORD_CHARACTER, ASCII) and NONE are excluded,
# declaration order preserved
ABBR_TAG_NODE_MEMBERS = tuple(
    tag
    for tag in AbbrTags
    if tag not in _EXCLUDED_ABBR_TAGS and bin(tag.value).count("1") == 1
)


def heading_for_abbr_tag(abbr_tag):
    """
    :param abbr_tag: member of ``ABBR_TAG_NODE_MEMBERS``
    :type abbr_tag: AbbrTags
    :return: heading text an ``AbbrTagNode`` for ``abbr_tag`` renders
            under, e.g. ``single_character`` -> ``"Single Character"``
    :rtype: str
    """
    return abbr_tag.name.replace("_", " ").title()


class AbbrTagNode(DynamicNode):  ################################################
    """
    dynamic node that provides every abbr entry tagged with a single
    ``AbbrTags`` member -- unlike the fixed set of dynamic node types in
    ``DYNAMIC_NODE_TYPES``, one instance is created per member of
    ``ABBR_TAG_NODE_MEMBERS``, parametrized at construction time
    (mirrors ``GlossaryNode``)
    """

    def __init__(self, parent=None, *, abbr_tag, preface=(), **kwargs):
        self.abbr_tag = abbr_tag
        self.HEADING = heading_for_abbr_tag(abbr_tag)  # implement DynamicNode
        super().__init__(parent, preface=preface, **kwargs)

    # implement BasePromptNode  ------------------------------------------------

    def content_lines(self, **kwargs):
        return self._preface + gen_shorthand_content_lines(self.abbr_tag)

    def __copy__(self):
        return type(self)(
            None, abbr_tag=self.abbr_tag, preface=self._preface
        )
