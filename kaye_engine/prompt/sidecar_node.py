"""
sidecar_node.py

nodes attached to a blueprint's parent node but stored as corpus content,
identified by the ``{name}`` heading convention; excluded by default and
conditionally spliced in via ``conditional_sidecars`` when their parent is
checkmarked
"""

import re

__all__ = (
    "AVOID_NAME",
    "get_sidecar_name",
)

# reserved descriptor names, documentation only; a blueprint's ``meta``
# points at these nodes by path
DESCRIPTION_NAME = "description"
WHEN_TO_USE_NAME = "when_to_use"
GLOBS_NAME = "globs"

# reserved but not a descriptor -- never read as a blueprint descriptor;
# discovered directly by render.render_negative_prompt_lines() at any depth
AVOID_NAME = "avoid"


# name detection  ##############################################################

_SIDECAR_HEADING_PATTERN = re.compile(r"^\{(.+)\}$")


def get_sidecar_name(node):
    """
    determine a node's sidecar name from its heading

    identifies a sidecar node by its ``{name}`` heading convention and
    returns the name inside the braces (e.g., ``description``,
    ``globs``). returns ``None`` if the node is not a sidecar node.

    **usage**:

    >>> from kaye_engine.prompt.sidecar_node import get_sidecar_name
    >>> name = get_sidecar_name(node)
    >>> if name is not None:
    ...     print(f"sidecar name: {name}")
    >>> if name == "Claude Tool:TodoWrite":
    ...     print("this is a conditional sidecar node")


    :param node: node to check (must have a ``name`` attribute)
    :type node: BasePromptNode
    :return: the sidecar name, or ``None`` if not a sidecar node
    :rtype: str or None
    """
    match = _SIDECAR_HEADING_PATTERN.match(node.name)
    return match.group(1) if match else None
