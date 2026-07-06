"""
sidecar_node_type.py

define ``SidecarNodeType`` as an ``IntFlag`` for sidecar node type operations
"""

from enum import IntFlag, auto


class SidecarNodeType(IntFlag):  ###############################################
    """
    represent sidecar node types using bitwise flag operations
    """

    NONE = 0
    DESCRIPTION = auto()
    WHEN_TO_USE = auto()
    GLOBS = auto()
    PREREQUISITE = auto()
    FOR_CLAUDE = auto()

    # check types  =============================================================

    @classmethod
    def is_sidecar_node_of_type(cls, node, sidecar_node_type):
        """
        check if a node matches any sidecar node type in the flags

        supports single types and combined flags. For combined flags like
        ``PREREQUISITE | FOR_CLAUDE``, returns ``True`` if node matches
        any of the individual types.


        :param node: the node to check (must have a ``name`` attribute)
        :type node: BasePromptNode
        :param sidecar_node_type: the ``SidecarNodeType`` flag(s) to match
        :type sidecar_node_type: SidecarNodeType
        :return: ``True`` if node's name matches any flag types
        :rtype: bool
        """
        if sidecar_node_type == cls.NONE:
            return False

        for flag in cls:
            if flag and flag != cls.NONE and (sidecar_node_type & flag):
                if node.name == flag.as_node_heading:
                    return True
        return False

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
        if self not in _HEADING_NAMES:
            raise ValueError(
                "combined flags {} have no node heading; "
                "only single types are valid".format(self)
            )
        return "{{{}}}".format(_HEADING_NAMES[self])


# constants  ###################################################################


_HEADING_NAMES = {
    SidecarNodeType.DESCRIPTION: "description",
    SidecarNodeType.WHEN_TO_USE: "when_to_use",
    SidecarNodeType.GLOBS: "globs",
    SidecarNodeType.PREREQUISITE: "prerequisite",
    SidecarNodeType.FOR_CLAUDE: "for_claude",
}
