from .base_prompt_node import DynamicNode

__all__ = ("QueryAbbrNode", "PLCNode")


class QueryAbbrNode(DynamicNode):
    """
    TODO docstring for class DynamicAbbrNode
    """

    HEADING = "Abbreviations"

    # constructor  =============================================================

    def __init__(self, parent):
        super().__init__(self.HEADING, parent)

    # implement BasePromptNode  ================================================

    @property
    def content_lines(self, **kwargs):
        pass  # TODO


class PLCNode(DynamicNode):
    """
    TODO docstring for class PLCNode
    """

    HEADING = "Programming Languages Code"

    # constructor  =============================================================

    def __init__(self, parent):
        super().__init__(self.HEADING, parent)

    # implement BasePromptNode  ================================================
    @property
    def content_lines(self, **kwargs):
        return []


# TODO usable abbrs node
