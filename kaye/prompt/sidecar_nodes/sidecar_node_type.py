"""
sidecar_node_type.py

define ``SidecarNodeType`` as an ``IntFlag`` for sidecar node type operations
"""

from enum import IntFlag, auto


class SidecarNodeType(IntFlag):  ###############################################
    """
    represent sidecar node types using bitwise flag operations

    sidecar node types are categorized into:

    - **Descriptor sidecars** (DESCRIPTION, WHEN_TO_USE, GLOBS): metadata
      about a parent node, exposed via blueprint.sidecars attribute
    - **Conditional sidecar nodes** (PREREQUISITE, FOR_CLAUDE): real prompt
      content conditionally included via contains_sidecar_nodes parameter

    **NONE** (value 0) indicates the node is not a sidecar node and evaluates
    to ``False`` in boolean context. Any other type evaluates to ``True``.

    **usage examples**:

    >>> from kaye.prompt.sidecar_nodes import get_sidecar_node_type
    >>> node_type = get_sidecar_node_type(node)
    >>> if bool(node_type):  # True if any sidecar type
    ...     pass
    >>> if node_type & (PREREQUISITE | FOR_CLAUDE):  # bitwise check
    ...     pass  # conditional sidecar node
    """

    NONE = 0
    DESCRIPTION = auto()
    WHEN_TO_USE = auto()
    GLOBS = auto()
    # FIXME make for claude & prerequisite generic terms
    PREREQUISITE = auto()  # conditional sidecar node type
    FOR_CLAUDE = auto()  # conditional sidecar node type

    # property  ================================================================

    @property
    def as_node_heading(self):
        """
        render this sidecar node type as a corpus node heading


        :raises ValueError: if called on ``NONE`` or combined flags
        :return: this sidecar node type rendered as a corpus node heading,
                e.g., ``{description}``
        :rtype: str
        """
        if self == self.NONE:
            raise ValueError("NONE has no node heading")
        if self not in SIDECAR_NODE_TYPE_HEADINGS:
            raise ValueError(
                "combined flags {} have no node heading; "
                "only single types are valid".format(self)
            )
        return "{{{}}}".format(SIDECAR_NODE_TYPE_HEADINGS[self])


# sidecar node type to heading name mapping  ##################################

SIDECAR_NODE_TYPE_HEADINGS = {
    SidecarNodeType.DESCRIPTION: "description",
    SidecarNodeType.WHEN_TO_USE: "when_to_use",
    SidecarNodeType.GLOBS: "globs",
    SidecarNodeType.PREREQUISITE: "prerequisite",
    SidecarNodeType.FOR_CLAUDE: "for_claude",
}
