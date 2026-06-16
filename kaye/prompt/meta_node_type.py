"""
meta_node_type.py

define ``MetaNodeType``
"""

from enum import Enum


class MetaNodeType(Enum):
    """
    represent a meta node type as ``Enum``
    """

    DESCRIPTION = "description"
    WHEN_TO_USE = "when_to_use"
    GLOBS = "globs"
    PREREQUISITE = "prerequisite"

    @property
    def as_node_heading(self):
        """
        :return: this meta node type rendered as a corpus node heading,
                e.g. ``"{description}"``
        :rtype: str
        """
        return "{{{}}}".format(self.value)
