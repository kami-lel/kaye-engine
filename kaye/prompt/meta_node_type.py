"""
meta_node_type.py

define ``MetaNodeType`` as an ``IntFlag`` for meta node type operations
"""

from enum import IntFlag, auto


class MetaNodeType(IntFlag):  ##################################################
    """
    represent meta node types using bitwise flag operations
    """

    NONE = 0
    DESCRIPTION = auto()
    WHEN_TO_USE = auto()
    GLOBS = auto()
    PREREQUISITE = auto()
    FOR_CLAUDE = auto()

    # check types  =============================================================

    @classmethod
    def is_meta_node_of_type(cls, node, meta_node_type):
        """
        check if a node matches any meta node type in the flags

        supports single types and combined flags. For combined flags like
        ``PREREQUISITE | FOR_CLAUDE``, returns ``True`` if node matches
        any of the individual types.


        :param node: the node to check (must have a ``name`` attribute)
        :type node: BasePromptNode
        :param meta_node_type: the ``MetaNodeType`` flag(s) to match
        :type meta_node_type: MetaNodeType
        :return: ``True`` if node's name matches any flag types
        :rtype: bool
        """
        if meta_node_type == cls.NONE:
            return False

        for flag in cls:
            if flag and flag != cls.NONE and (meta_node_type & flag):
                if node.name == flag.as_node_heading:
                    return True
        return False

    # property  ================================================================

    @property
    def as_node_heading(self):
        """
        render this meta node type as a corpus node heading


        :raises ValueError: if called on ``NONE`` or combined flags
        :return: this meta node type rendered as a corpus node heading,
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
    MetaNodeType.DESCRIPTION: "description",
    MetaNodeType.WHEN_TO_USE: "when_to_use",
    MetaNodeType.GLOBS: "globs",
    MetaNodeType.PREREQUISITE: "prerequisite",
    MetaNodeType.FOR_CLAUDE: "for_claude",
}
