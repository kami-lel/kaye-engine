__all__ = ("QueryAbbrNode", "PLCNode")


class QueryAbbrNode:
    """
    TODO docstring for class DynamicAbbrNode
    """


class PLCNode:
    """
    TODO docstring for class PLCNode
    """

    HEADING = "Programming Languages Code"

    # constructor  =============================================================

    def __init__(self, parent):
        super().__init__(self.HEADING, parent)

    # implement BasePromptNode  ================================================
    @property
    def content_lines(self):
        pass  # TODO


# TODO usable abbrs node
