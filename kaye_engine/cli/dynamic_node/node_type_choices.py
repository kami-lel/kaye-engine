"""
node_type_choices.py

define ``ENGINE_DEFINED_NODES``, ``get_node_type_choices``, and
``gen_node_type_list``
"""

from kaye_engine.abbr_collection import get_abbr_data
from kaye_engine.prompt.dynamic_nodes import AbbrGroupNode, AbbrNode, TodayNode

__all__ = (
    "ENGINE_DEFINED_NODES",
    "gen_node_type_list",
    "get_node_type_choices",
)

# constants  ###################################################################
ENGINE_DEFINED_NODES = {
    "today": TodayNode,
    "abbr": AbbrNode,
}


# Public API  ##################################################################
def get_node_type_choices():
    """
    :return: every currently resolvable ``NODE_TYPE`` value mapped to
            its dynamic node class -- ``ENGINE_DEFINED_NODES`` plus one
            ``AbbrGroupNode`` entry per abbr group name currently known
            to ``get_abbr_data().groups``
    :rtype: dict{str: type}
    """
    choices = dict(ENGINE_DEFINED_NODES)
    for group_name in get_abbr_data().groups.names:
        choices[group_name] = AbbrGroupNode
    return choices


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
    lines += [
        "{:<14} {}".format(group_name, group_name)
        for group_name in get_abbr_data().groups.names
    ]
    return "\n".join(lines)
