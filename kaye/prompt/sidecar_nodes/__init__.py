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
    "is_sidecar_node",
    "SidecarNodeType",
    "BlueprintDescriptorSidecars",
)


def is_sidecar_node(node):
    """
    check if a node is a **sidecar node**

    :param node: node to check
    :type node: BasePromptNode
    :return: ``True`` if node's name matches sidecar convention ``{name}``
    :rtype: bool
    """
    return bool(re.match(r"^\{.+\}$", node.name))
