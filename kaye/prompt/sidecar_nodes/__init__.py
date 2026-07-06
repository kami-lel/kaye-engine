"""
sidecar_nodes

nodes attached to a blueprint's parent node but stored as corpus content,
identified by the ``{name}`` heading convention; excluded by default and
conditionally spliced in via ``contains_sidecar_nodes`` when their parent is
checkmarked
"""

import re

from .sidecar_node_type import SidecarNodeType
from .blueprint_description_sidecars import BlueprintDescriptorSidecars

__all__ = (
    "get_sidecar_node_type",
    "SidecarNodeType",
    "BlueprintDescriptorSidecars",
)


# constants  ###################################################################

SIDECAR_NODE_TYPE_HEADINGS = {
    SidecarNodeType.DESCRIPTION: "description",
    SidecarNodeType.WHEN_TO_USE: "when_to_use",
    SidecarNodeType.GLOBS: "globs",
    SidecarNodeType.PREREQUISITE: "prerequisite",
    SidecarNodeType.FOR_CLAUDE: "for_claude",
}


# type detection  #############################################################


def get_sidecar_node_type(node):
    """
    determine the sidecar node type from a node's name

    matches the node's name against the sidecar naming convention
    ``{name}`` and identifies its specific type. if the node is not a
    recognized sidecar node, returns ``SidecarNodeType.NONE``.


    :param node: node to check (must have a ``name`` attribute)
    :type node: BasePromptNode
    :return: sidecar node type (NONE if not a sidecar node)
    :rtype: SidecarNodeType
    """
    if not re.match(r"^\{.+\}$", node.name):
        return SidecarNodeType.NONE

    for node_type, heading_name in SIDECAR_NODE_TYPE_HEADINGS.items():
        if node.name == "{{{}}}".format(heading_name):
            return node_type

    return SidecarNodeType.NONE
