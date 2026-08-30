"""
dynamic_nodes

node types whose content has no fixed value and is generated during
``.generate_prompt_without_dependencies()`` (e.g. today's date/time,
shorthand present in a query)
"""

from .abbr_tag_node import ABBR_TAG_NODE_MEMBERS, AbbrTagNode, slug_for_abbr_tag
from .decode_only_abbr_node import DecodeOnlyAbbrNode
from .dynamic_node import DynamicNode
from .glossary_node import GlossaryNode, gen_glossary_content_lines
from .shorthand_tag_nodes import gen_shorthand_content_lines
from .today_node import TodayNode

__all__ = (
    "ABBR_TAG_NODE_MEMBERS",
    "DYNAMIC_NODE_TYPES",
    "AbbrTagNode",
    "DecodeOnlyAbbrNode",
    "DynamicNode",
    "GlossaryNode",
    "TodayNode",
    "gen_glossary_content_lines",
    "gen_shorthand_content_lines",
    "resolve_dynamic_node_factory",
    "slug_for_abbr_tag",
)

# registry of every engine-defined, statically-registered dynamic node
DYNAMIC_NODE_TYPES = (
    TodayNode,
    DecodeOnlyAbbrNode,
)

from .registry import (
    resolve_dynamic_node_factory,
)  # noqa: E402  (avoids circular import)
