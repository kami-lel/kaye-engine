"""
dynamic_nodes

node types whose content has no fixed value and is generated during
``.generate_prompt()`` (e.g. today's date/time, abbreviations present in a
query)
"""

from .abbr_nodes import AbbrNode
from .abbr_tag_nodes import gen_abbrs_content_lines
from .dynamic_node import DynamicNode
from .glossary_node import GlossaryNode, gen_glossary_content_lines
from .today_node import TodayNode

__all__ = (
    "DYNAMIC_NODE_TYPES",
    "AbbrNode",
    "DynamicNode",
    "GlossaryNode",
    "TodayNode",
    "gen_abbrs_content_lines",
    "gen_glossary_content_lines",
)

# registry of every engine-defined, statically-registered dynamic node
DYNAMIC_NODE_TYPES = (
    TodayNode,
    AbbrNode,
)
