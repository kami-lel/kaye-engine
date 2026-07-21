"""
sidecar_nodes

nodes attached to a blueprint's parent node but stored as corpus content,
identified by the ``{name}`` heading convention; excluded by default and
conditionally spliced in via ``contains_sidecars`` when their parent is
checkmarked
"""

import re

from .blueprint_description_sidecars import BlueprintDescriptorSidecars

__all__ = (
    "get_sidecar_name",
    "BlueprintDescriptorSidecars",
)


# name detection  ##############################################################

_SIDECAR_HEADING_PATTERN = re.compile(r"^\{(.+)\}$")


def get_sidecar_name(node):
    """
    determine a node's sidecar name from its heading

    identifies a sidecar node by its ``{name}`` heading convention and
    returns the name inside the braces (e.g., ``description``,
    ``prerequisite``). returns ``None`` if the node is not a sidecar node.

    **usage**:

    >>> from kaye.prompt.sidecar_nodes import get_sidecar_name
    >>> name = get_sidecar_name(node)
    >>> if name is not None:
    ...     print(f"sidecar name: {name}")
    >>> if name in ("prerequisite", "for claude code"):
    ...     print("this is a conditional sidecar node")


    :param node: node to check (must have a ``name`` attribute)
    :type node: BasePromptNode
    :return: the sidecar name, or ``None`` if not a sidecar node
    :rtype: str or None
    """
    match = _SIDECAR_HEADING_PATTERN.match(node.name)
    return match.group(1) if match else None
