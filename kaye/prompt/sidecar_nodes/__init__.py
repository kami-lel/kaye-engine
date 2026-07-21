"""
sidecar_nodes

nodes attached to a blueprint's parent node but stored as corpus content,
identified by the ``{name}`` heading convention; excluded by default and
conditionally spliced in via ``contains_sidecar_tags`` when their parent is
checkmarked
"""

import re

from .blueprint_description_sidecars import BlueprintDescriptorSidecars

__all__ = (
    "get_sidecar_tag",
    "BlueprintDescriptorSidecars",
)


# tag detection  ###############################################################

_SIDECAR_HEADING_PATTERN = re.compile(r"^\{(.+)\}$")


def get_sidecar_tag(node):
    """
    determine a node's sidecar tag from its name

    identifies a sidecar node by its ``{name}`` heading convention and
    returns the tag inside the braces (e.g., ``description``,
    ``prerequisite``). returns ``None`` if the node is not a sidecar node.

    **usage**:

    >>> from kaye.prompt.sidecar_nodes import get_sidecar_tag
    >>> tag = get_sidecar_tag(node)
    >>> if tag is not None:
    ...     print(f"sidecar tag: {tag}")
    >>> if tag in ("prerequisite", "for-claude-code"):
    ...     print("this is a conditional sidecar node")


    :param node: node to check (must have a ``name`` attribute)
    :type node: BasePromptNode
    :return: the sidecar tag, or ``None`` if not a sidecar node
    :rtype: str or None
    """
    match = _SIDECAR_HEADING_PATTERN.match(node.name)
    return match.group(1) if match else None
