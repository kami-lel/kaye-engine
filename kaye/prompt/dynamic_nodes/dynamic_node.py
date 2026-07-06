"""
dynamic_node.py

define ``DynamicNode``
"""

import re

from kaye.prompt.base_prompt_node import BasePromptNode

__all__ = ("DynamicNode",)


# FIXME FIXME refactorize dynamic node


class DynamicNode(BasePromptNode):  # pylint: disable=abstract-method
    """
    abstract class for all *dynamic node*
    """

    @classmethod
    def is_valid_dynamic_node_heading(cls, heading):
        """
        :param heading:
        :type heading: str
        :return: whether a node's heading fits dynamic node's heading syntax
        :rtype: bool
        """
        return cls._ID_PATTERN.match(heading)

    # constructor  =============================================================
    def __init__(self, parent=None, **kwargs):
        heading = "(" + self.HEADING + ")"
        super().__init__(heading, parent=parent, **kwargs)

    _ID_PATTERN = re.compile(r"^\(.+\)$")

    HEADING = None

    # implement BasePromptNode  ================================================

    def _pre_attach_children(self, children):
        # dynamic node must be leaf node
        if len(children) != 0:
            raise TypeError("{} must be leaf node".format(type(self)))

    def __copy__(self):
        return type(self)(None)
