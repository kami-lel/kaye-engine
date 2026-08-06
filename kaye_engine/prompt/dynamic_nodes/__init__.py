"""
dynamic_nodes

node types whose content has no fixed value and is generated during
``.generate_prompt()`` (e.g. today's date/time, abbreviations present in a
query)
"""

from .dynamic_node import DynamicNode
from .today_node import TodayNode
from .abbr_nodes import AbbrNode
from .abbr_tag_nodes import gen_abbrs_content_lines
from .abbr_group_node import gen_group_abbrs_content_lines, AbbrGroupNode

__all__ = (
    "gen_abbrs_content_lines",
    "gen_group_abbrs_content_lines",
    "DynamicNode",
    "TodayNode",
    "AbbrNode",
    "AbbrGroupNode",
    "DYNAMIC_NODE_TYPES",
)

# registry of every engine-defined, statically-registered dynamic node
DYNAMIC_NODE_TYPES = (
    TodayNode,
    AbbrNode,
)
