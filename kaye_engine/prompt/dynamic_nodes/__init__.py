"""
dynamic_nodes

node types whose content has no fixed value and is generated during
``.generate_prompt()`` (e.g. today's date/time, shorthand present in a
query)
"""

from .shorthand_node import ShorthandNode
from .shorthand_tag_nodes import gen_shorthand_content_lines
from .dynamic_node import DynamicNode
from .abbr_tag_node import AbbrTagNode, ABBR_TAG_NODE_MEMBERS, slug_for_abbr_tag
from .glossary_node import GlossaryNode, gen_glossary_content_lines
from .today_node import TodayNode

__all__ = (
    "DYNAMIC_NODE_TYPES",
    "ShorthandNode",
    "DynamicNode",
    "AbbrTagNode",
    "ABBR_TAG_NODE_MEMBERS",
    "slug_for_abbr_tag",
    "GlossaryNode",
    "TodayNode",
    "gen_shorthand_content_lines",
    "gen_glossary_content_lines",
    "resolve_dynamic_node_factory",
)

# registry of every engine-defined, statically-registered dynamic node
DYNAMIC_NODE_TYPES = (
    TodayNode,
    ShorthandNode,
)

from .registry import resolve_dynamic_node_factory  # noqa: E402  (avoids circular import)
