"""
dynamic_node.py

define ``DynamicNode``
"""

from kaye_engine.prompt.base_prompt_node import BasePromptNode

__all__ = ("DynamicNode",)


class DynamicNode(BasePromptNode):  # pylint: disable=abstract-method
    """
    abstract class for all *dynamic node*
    """

    # constructor  -------------------------------------------------------------
    def __init__(self, parent=None, preface=(), **kwargs):
        heading = "(" + self.NAME + ")"
        super().__init__(heading, parent=parent, **kwargs)

        self._preface = list(preface)

    # abstract fields  ---------------------------------------------------------

    NAME = None

    # implement BasePromptNode  ------------------------------------------------

    def _pre_attach_children(self, children):
        # dynamic node must be leaf node
        if len(children) != 0:
            raise TypeError("{} must be leaf node".format(type(self)))

    def __copy__(self):
        return type(self)(None, preface=self._preface)
