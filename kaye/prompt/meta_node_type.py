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

    # TODO add {claude} subnode

    # check types  =============================================================

    @classmethod
    def is_meta_node(cls, node, meta_node_type):
        """
        Check if a node is of a specific meta node type.


        :param node: the node to check (must have a ``name`` attribute)
        :type node: BasePromptNode
        :param meta_node_type: the MetaNodeType to match against
        :type meta_node_type: MetaNodeType
        :return: True if the node's name matches the meta node type heading
        :rtype: bool
        """
        return node.name == meta_node_type.as_node_heading

    @classmethod
    def is_description(cls, node):
        """
        Check if a node is a {description} meta node.


        :param node: the node to check
        :type node: BasePromptNode
        :return: True if the node is a description meta node
        :rtype: bool
        """
        return cls.is_meta_node(node, cls.DESCRIPTION)

    @classmethod
    def is_when_to_use(cls, node):
        """
        Check if a node is a {when_to_use} meta node.


        :param node: the node to check
        :type node: BasePromptNode
        :return: True if the node is a when_to_use meta node
        :rtype: bool
        """
        return cls.is_meta_node(node, cls.WHEN_TO_USE)

    @classmethod
    def is_globs(cls, node):
        """
        Check if a node is a {globs} meta node.


        :param node: the node to check
        :type node: BasePromptNode
        :return: True if the node is a globs meta node
        :rtype: bool
        """
        return cls.is_meta_node(node, cls.GLOBS)

    @classmethod
    def is_prerequisite(cls, node):
        """
        Check if a node is a {prerequisite} meta node.


        :param node: the node to check
        :type node: BasePromptNode
        :return: True if the node is a prerequisite meta node
        :rtype: bool
        """
        return cls.is_meta_node(node, cls.PREREQUISITE)

    # property  ================================================================

    @property
    def as_node_heading(self):
        """
        :return: this meta node type rendered as a corpus node heading,
                e.g. ``"{description}"``
        :rtype: str
        """
        return "{{{}}}".format(self.value)
