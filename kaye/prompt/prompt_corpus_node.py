"""
prompt_corpus_node.py

define ``PromptCorpusNode``
"""

from .base_prompt_node import BasePromptNode
from .dynamic_nodes import is_valid_dynamic_node_heading

# section heading prefix used for parsing .md file of prompt corpus

__all__ = ("PromptCorpusNode",)


class PromptCorpusNode(BasePromptNode):
    """
    A `PromptCorpusNode` encapsule a single node in the *prompt corpus tree*.


    :param heading: section heading, i.e. node name
    :type heading: str
    :param parent: parent node in the tree structure;
            `None` if the root node
    :type parent: PromptCorpusNode
    :param content_lines: section content, each ``str`` represents a line
    :type content_lines: list(str)
    :example:
    >>> tree = PromptCorpusNode.parse(prompt_corpus_text)
    """

    # constructor  =============================================================
    def __init__(self, heading, parent, content_lines):
        # check valid name
        if is_valid_dynamic_node_heading(heading):
            raise ValueError("illegal heading syntax: {}".format(repr(heading)))

        super().__init__(heading, parent)

        self._content_lines = content_lines

    # implement BasePromptNode  ================================================

    def content_lines(self, **kwargs):
        return self._content_lines

    def __copy__(self):
        copied = type(self)(self.name, None, [])
        copied._content_lines = self._content_lines
        return copied
