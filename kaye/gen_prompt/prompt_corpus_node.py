"""
define ``PromptCorpusNode``
"""

import re

from .base_prompt_node import BasePromptNode

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
        self._init_check_name(heading)

        super().__init__(heading, parent)

        # trim leading/trailing empty strings
        start, end = 0, len(content_lines)
        while start < end and content_lines[start] == "":
            start += 1
        while end > start and content_lines[end - 1] == "":
            end -= 1
        self._content_lines = content_lines[start:end]

    # constructor helpers  *****************************************************
    HEADING_FORBIDDEN = re.compile(r"{.*}")

    @classmethod
    def _init_check_name(cls, name):
        """
        test name to be a legal heading

        (helper method used in ``__init__()``)
        """
        if cls.HEADING_FORBIDDEN.fullmatch(name):
            raise ValueError("illegal heading syntax: {}".format(repr(name)))

    # implement BasePromptNode  ================================================

    @property
    def id(self):
        # for PromptCorpusNode, identical to heading
        return self.name

    def content_lines(self, **kwargs):
        return self._content_lines

    def __copy__(self):
        obj = type(self)(self.name, self.parent, [])
        obj._content_lines = self._content_lines
        return obj

    # Hack rm
    # def _generate_prompt_lines(self):
    #     """
    #     generate prompt lines as this node appeared in concrete prompt

    #     (helper method used in ``PromptBlueprint.generate_prompt()``)

    #     :return: lines of prompt
    #     :rtype: list[str]
    #     """
    #     lines = [""]  # add empty lines before headings
    #     # heading line
    #     lines.append(HEADING_PREFIX * self.depth + " " + self.name)
    #     # content lines
    #     lines.extend(self.content)

    #     return lines
