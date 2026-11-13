"""
node_type_choices.py

define ``ENGINE_DEFINED_NODES`` and ``list_all_node_type_names``
"""

from kaye_engine.abbr_collection import abbr_glossary_registry
from kaye_engine.prompt.dynamic_nodes import (
    ABBR_TAG_NODE_MEMBERS,
    DecodeOnlyAbbrNode,
    TodayNode,
    slug_for_abbr_tag,
)

__all__ = (
    "ENGINE_DEFINED_NODES",
    "list_all_node_type_names",
)

# constants  ###################################################################
ENGINE_DEFINED_NODES = {
    "today": TodayNode,
    "decode-only-abbr": DecodeOnlyAbbrNode,
}


# Public API  ##################################################################
def list_all_node_type_names():
    """
    :return: every currently available ``NODE_TYPE`` name, in 2 sorted
            runs: the engine-defined names and every ``AbbrTagNode`` kebab
            slug, then every registered abbr glossary name
    :rtype: list[str]
    """
    return sorted(
        [*ENGINE_DEFINED_NODES]
        + [slug_for_abbr_tag(abbr_tag) for abbr_tag in ABBR_TAG_NODE_MEMBERS]
    ) + sorted(abbr_glossary_registry)
