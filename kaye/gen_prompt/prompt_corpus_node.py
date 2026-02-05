"""
define ``PromptCorpusNode``
"""

import re

from .base_prompt_node import BasePromptNode

# section heading prefix used for parsing .md file of prompt corpus
HEADING_PREFIX = "#"
ROOT_NODE_NAME = "○"  # placeholder name for root node

__all__ = ("PromptCorpusNode",)


class PromptCorpusNode(BasePromptNode):

    # public API  ==============================================================

    @staticmethod
    def parse_prompt_corpus(prompt_corpus_text):
        pass  # TODO

    # constructor  =============================================================
    # constructor helpers  *****************************************************

    # implement BasePromptNode  ================================================
    @property
    def id(self):
        # for PromptCorpusNode, identical to heading
        return self.name


class PromptCorpusNodeLegacy(BasePromptNode):
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
        # TODO ban use of {heading}

        # reduce formatting empty lines
        text_cleanup = re.sub(r"\n{3,}", "\n\n", prompt_corpus_text)
        text_lines = list(text_cleanup.split("\n"))

        root = cls(ROOT_NODE_NAME, None, text_lines)
        return root

    # constructor  =============================================================
    def __init__(self, name, parent, text_lines=None):
        super().__init__(name, parent)
        self.content = []  # content lines

        self.path_of_names = self._init_generate_path_of_names()

        if text_lines is None:
            return

        self._init_populate_children(text_lines)

        # trim leading/trailing empty strings
        start, end = 0, len(self.content)
        while start < end and self.content[start] == "":
            start += 1
        while end > start and self.content[end - 1] == "":
            end -= 1
        self.content = self.content[start:end]

    # helper methods  ==========================================================

    def _init_populate_children(self, text_lines):
        """
        helper method used in ``__init__()``


        create children nodes of ``self`` and populate self.content
        by parsing ``text_lines``
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
            self.content = list(text_lines)
            return

        # this node contains subsections, then parse the content part out
        self.content = text_lines[: heading_lines[0]]
        if not any(self.content):
            self.content = []

        # parse sub-sections as nodes
        heading_lines.append(len(text_lines))
        for start, end in zip(heading_lines, heading_lines[1:]):
            # extract heading content
            # e.g. "### this is heading " -> "this is heading"
            heading_content = text_lines[start][len(heading_prefix) :].strip()
            children_nodes = text_lines[start + 1 : end]
            PromptCorpusNode(heading_content, self, children_nodes)

    def _generate_prompt_lines(self):
        """
        generate prompt lines as this node appeared in concrete prompt

        (helper method used in ``PromptBlueprint.generate_prompt()``)


        :return: lines of prompt
        :rtype: list[str]
        """
        lines = [""]  # add empty lines before headings
        # heading line
        lines.append(HEADING_PREFIX * self.depth + " " + self.name)
        # content lines
        lines.extend(self.content)

        return lines

    # magic methods  ===========================================================

    def __copy__(self):
        """
        :return: a copy without any children
        :rtype: PromptCorpusNode
        """
        obj = PromptCorpusNode(self.name, self.parent, None)
        obj.content = self.content
        return obj
