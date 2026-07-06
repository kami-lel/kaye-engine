"""
dynamic_nodes

node types whose content has no fixed value and is generated during
``.generate_prompt()`` (e.g. today's date/time, abbreviations present in a
query)
"""

import re

from .dynamic_node import DynamicNode
from .today_node import TodayNode
from .abbr_nodes import AbbrNode
from .abbr_tag_nodes import (
    UsableAbbrNode,
    LanguageCodeNode,
    PLCNode,
    UnityEngineAbbrNode,
    CodingTermsNode,
)

__all__ = (
    "is_valid_dynamic_node_heading",
    "DynamicNode",
    "TodayNode",
    "AbbrNode",
    "UsableAbbrNode",
    "LanguageCodeNode",
    "PLCNode",
    "UnityEngineAbbrNode",
    "CodingTermsNode",
    "DYNAMIC_NODE_TYPES",
)

# registry of every dynamic node type attached to the prompt corpus tree
DYNAMIC_NODE_TYPES = (
    TodayNode,
    AbbrNode,
    UsableAbbrNode,
    LanguageCodeNode,
    PLCNode,
    UnityEngineAbbrNode,
    CodingTermsNode,
)


_DYNAMIC_NODE_HEADING_PATTERN = re.compile(r"^\(.+\)$")


# Public Function  #############################################################


def is_valid_dynamic_node_heading(heading):
    """
    :param heading: a node's heading to check
    :type heading: str
    :return: whether ``heading`` fits dynamic node's heading syntax
    :rtype: bool
    """
    return bool(_DYNAMIC_NODE_HEADING_PATTERN.match(heading))
