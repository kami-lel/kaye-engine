"""
node_type_choices.py

define ``ENGINE_DEFINED_NODES`` and ``list_all_node_type_names``
"""

from kaye_engine.abbr_collection import abbr_group_registry
from kaye_engine.prompt.dynamic_nodes import AbbrNode, TodayNode

__all__ = (
    "ENGINE_DEFINED_NODES",
    "list_all_node_type_names",
)

# constants  ###################################################################
ENGINE_DEFINED_NODES = {
    "today": TodayNode,
    "abbr": AbbrNode,
}


# Public API  ##################################################################
def list_all_node_type_names():
    """
    :return: every currently available ``NODE_TYPE`` name -- the
            engine-defined names and every registered abbr group name --
            sorted alphabetically
    :rtype: list[str]
    """
    return sorted(set(ENGINE_DEFINED_NODES) | set(abbr_group_registry))
