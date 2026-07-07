"""
dynamic_node.py

define ``DynamicNode``
"""

from kaye.prompt.base_prompt_node import BasePromptNode

__all__ = ("DynamicNode",)


class DynamicNode(BasePromptNode):  # pylint: disable=abstract-method
    """
    abstract class for all *dynamic node*
    """

    # constructor  -------------------------------------------------------------
    def __init__(self, parent=None, **kwargs):
        heading = "(" + self.HEADING + ")"
        super().__init__(heading, parent=parent, **kwargs)

    # abstract fields  ---------------------------------------------------------

    HEADING = None

    # implement BasePromptNode  ------------------------------------------------

    def _pre_attach_children(self, children):
        # dynamic node must be leaf node
        if len(children) != 0:
            raise TypeError("{} must be leaf node".format(type(self)))

    def __copy__(self):
        return type(self)(None)
