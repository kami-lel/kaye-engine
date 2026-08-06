"""
node_type_choices.py

define ``ENGINE_DEFINED_NODES`` and ``gen_node_type_list``
"""

from kaye_engine.abbr_collection import get_abbr_data
from kaye_engine.prompt.dynamic_nodes import AbbrNode, TodayNode

__all__ = (
    "ENGINE_DEFINED_NODES",
    "gen_node_type_list",
)

# constants  ###################################################################
ENGINE_DEFINED_NODES = {
    "today": TodayNode,
    "abbr": AbbrNode,
}


# Public API  ##################################################################
def gen_node_type_list():
    """
    :return: one ``"NAME    HEADING"`` line per currently resolvable
            ``NODE_TYPE`` value, for use in CLI help/description text
    :rtype: str
    """
    lines = [
        "{:<14} {}".format(name, cls.HEADING)
        for name, cls in ENGINE_DEFINED_NODES.items()
    ]
    lines += sorted(get_abbr_data().groups.names)
    return "\n".join(lines)
