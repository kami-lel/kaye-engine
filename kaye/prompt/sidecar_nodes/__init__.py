"""
sidecar_nodes

nodes attached to a blueprint's parent node but stored as corpus content,
identified by the ``{name}`` heading convention; excluded by default and
conditionally spliced in via ``contains_sidecar_nodes`` when their parent is
checkmarked
"""

import re

from .sidecar_node_type import SidecarNodeType, _SIDECAR_NODE_TYPE_HEADINGS
from .blueprint_description_sidecars import BlueprintDescriptorSidecars

__all__ = (
    "get_sidecar_node_type",
    "SidecarNodeType",
    "BlueprintDescriptorSidecars",
    "SIDECAR_NODE_TYPE_HEADINGS",
)


# constants (re-exported from sidecar_node_type)  ##############################

SIDECAR_NODE_TYPE_HEADINGS = _SIDECAR_NODE_TYPE_HEADINGS


# type detection  #############################################################


def get_sidecar_node_type(node):
    """
    determine the sidecar node type from a node's name

    identifies the type of a sidecar node by matching its name against
    known sidecar node type headings (e.g., ``{description}``,
    ``{prerequisite}``). returns ``SidecarNodeType.NONE`` (which evaluates
    to ``False`` in boolean context) if the node is not a recognized sidecar
    node type.

    **usage**:

    >>> from kaye.prompt.sidecar_nodes import get_sidecar_node_type
    >>> node_type = get_sidecar_node_type(node)
    >>> if bool(node_type):  # equivalent to: if node_type != NONE
    ...     print(f"sidecar node type: {node_type.name}")
    >>> if node_type & SidecarNodeType.PREREQUISITE:  # check for specific type
    ...     print("this is a conditional sidecar node")


    :param node: node to check (must have a ``name`` attribute)
    :type node: BasePromptNode
    :return: sidecar node type; ``SidecarNodeType.NONE`` (0) if not a
            sidecar node or unknown type
    :rtype: SidecarNodeType
    """
    if not re.match(r"^\{.+\}$", node.name):
        return SidecarNodeType.NONE

    for node_type, heading_name in SIDECAR_NODE_TYPE_HEADINGS.items():
        if node.name == "{{{}}}".format(heading_name):
            return node_type

    return SidecarNodeType.NONE
