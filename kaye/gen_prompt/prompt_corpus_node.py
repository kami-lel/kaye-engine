"""
define ``PromptCorpusNode``
"""

import re

from .base_prompt_node import BasePromptNode

# section heading prefix used for parsing .md file of prompt corpus
HEADING_PREFIX = "#"
ROOT_NODE_NAME = "○"  # placeholder name for root node

__all__ = ("PromptCorpusNode",)

# FIXME all docstring

HEADING_FORBIDDEN = re.compile(r"[{}#]")


class PromptCorpusNode(BasePromptNode):
    """
    A `PromptCorpusNode` encapsule a single node in the *prompt corpus tree*.


    :param name: section heading of the node
    :type name: str
    :param parent: parent node in the tree structure;
            `None` if the root node
    :type parent: PromptCorpusNode
    :param text_lines: content to be parsed, each ``str`` represents a line
    :type text_lines: list(str)
    :example:
    >>> tree = PromptCorpusNode.parse(prompt_corpus_text)
    """

    # public API  ==============================================================

    @classmethod
    def parse(cls, prompt_corpus_text):
        """
        parse *prompt corpus* text into the tree structure.


        :param prompt_corpus_text: full source *prompt corpus* content
        :type prompt_corpus_text: str
        :return: **root node** of the parsed *prompt corpus* tree structure
        :rtype: PromptCorpusNode
        """
        # reduce 2+ empty lines into single empty line
        text_cleanup = re.sub(r"\n{3,}", "\n\n", prompt_corpus_text)
        # split to lines
        text_lines = list(text_cleanup.split("\n"))

        print(text_lines)  # HACK

        root = cls(ROOT_NODE_NAME, None, text_lines)
        return root

    # constructor  =============================================================
    def __init__(self, name, parent, text_lines=None):
        if HEADING_FORBIDDEN.match(name):
            # TODO unit test
            raise ValueError(
                "detects illegal symbol in heading: {}".format(repr(name))
            )

        super().__init__(name, parent)
        self._content_lines = []

        if text_lines is None:
            return

        self._init_populate_children(text_lines)

        # trim leading/trailing empty strings
        start, end = 0, len(self._content_lines)
        while start < end and self._content_lines[start] == "":
            start += 1
        while end > start and self._content_lines[end - 1] == "":
            end -= 1
        self._content_lines = self._content_lines[start:end]

    # constructor helpers  *****************************************************
    def _init_populate_children(self, text_lines):
        """
        create node children and add content to ``._content_line``

        (helper method used in ``__init__()``)
        """
        # find every sub-section heading lines
        heading_prefix = HEADING_PREFIX * (self.depth + 1) + " "
        heading_lines = []
        for idx, line in enumerate(text_lines):
            if line.startswith(heading_prefix):
                heading_lines.append(idx)

        # contain no subsection
        if not heading_lines:
            # all lines are content
            self._content_lines = list(text_lines)
            return

        # this node contains subsections, then parse the content part out
        self._content_lines = text_lines[: heading_lines[0]]
        if not any(self._content_lines):
            self._content_lines = []

        # parse sub-sections as nodes
        heading_lines.append(len(text_lines))
        for start, end in zip(heading_lines, heading_lines[1:]):
            # extract heading content
            # e.g. "### this is heading " -> "this is heading"
            heading_content = text_lines[start][len(heading_prefix) :].strip()
            children_nodes = text_lines[start + 1 : end]
            PromptCorpusNode(heading_content, self, children_nodes)

    # implement BasePromptNode  ================================================

    @property
    def id(self):
        # for PromptCorpusNode, identical to heading
        return self.name

    @property
    def content_lines(self):
        return self._content_lines

    # magic methods  ===========================================================

    def __copy__(self):
        """
        :return: a copy without any children
        :rtype: PromptCorpusNode
        """
        obj = type(self)(self.name, self.parent, [])
        obj._content_lines = self._content_lines
        return obj

    # HACK
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
