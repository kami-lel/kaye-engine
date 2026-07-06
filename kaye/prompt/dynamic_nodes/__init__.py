"""
dynamic_nodes

node types whose content has no fixed value and is generated during
``.generate_prompt()`` (e.g. today's date/time, abbreviations present in a
query)
"""

from .dynamic_node import DynamicNode
from .today_node import TodayNode
from .abbr_nodes import (
    AbbrNode,
    UsableAbbrNode,
    LanguageCodeNode,
    PLCNode,
    UnityEngineAbbrNode,
)

__all__ = (
    "DynamicNode",
    "TodayNode",
    "AbbrNode",
    "UsableAbbrNode",
    "LanguageCodeNode",
    "PLCNode",
    "UnityEngineAbbrNode",
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
)


# TODO abbr tag node
