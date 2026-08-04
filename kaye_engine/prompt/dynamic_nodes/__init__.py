"""
dynamic_nodes

node types whose content has no fixed value and is generated during
``.generate_prompt()`` (e.g. today's date/time, abbreviations present in a
query)
"""

from .dynamic_node import DynamicNode
from .today_node import TodayNode
from .abbr_nodes import AbbrNode
from .abbr_tag_nodes import (
    gen_abbrs_content_lines,
    UsableAbbrNode,
    LanguageCodeNode,
    PLCNode,
    UnityEngineAbbrNode,
    CodingTermsNode,
    PlanStepByStepAbbrNode,
)

__all__ = (
    "gen_abbrs_content_lines",
    "DynamicNode",
    "TodayNode",
    "AbbrNode",
    "UsableAbbrNode",
    "LanguageCodeNode",
    "PLCNode",
    "UnityEngineAbbrNode",
    "CodingTermsNode",
    "PlanStepByStepAbbrNode",
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
    PlanStepByStepAbbrNode,
)
