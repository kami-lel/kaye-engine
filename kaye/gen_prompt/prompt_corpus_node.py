"""
define ``PromptCorpusNode``
"""

import re

from anytree import RenderTree

from .base_prompt_corpus_node import BasePromptNode

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
    def name_in_lineage(self):
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

    def generate_preview_tree(
        self, preview_line_count=3, preview_line_width=64
    ):
        """
        generate **preview tree** of ``self`` as root,
        an human-readable representation


        :param preview_line_count: set maximum line count of
                *content preview* part, (excluding section heading line);
                defaults to 3
        :type preview_line_count: int
        :param preview_line_width: set maximum column width of
                *content preview* part;
                defaults to 64.
        :type preview_line_width: int
        :return: the preview tree
        :rtype: str
        :example:
        >>> tree.generate_preview_tree()
        ○
        └── Project Title
            ├── Description
            │   A brief overview of the project, its purpose, and goals.
            ├── Installation
            │   1. Clone the repo
            │   2. Install dependencies
            │   3. Run the application
            ├── Usage
            │   Provide instructions on how to use the application.
            ├── Contributing
            │   1. Fork the repo
            │   2. Create a new branch
            │   3. Submit a pull request
            └── License
                This project is licensed under the MIT License.
        >>> tree.generate_preview_tree(preview_line_count=0)
        ○
        └── Project Title
            ├── Description
            ├── Installation
            ├── Usage
            ├── Contributing
            └── License
        """
        opt_lines = []

        for pre, fill, node in RenderTree(self):
            # line for tree structure
            opt_lines.append(pre + node.name)
            # lines for node content preview
            opt_lines.extend(
                # pylint: disable=protected-access
                node._generate_preview_tree_content_preview_lines(
                    fill, preview_line_count, preview_line_width
                )
            )

        return "\n".join(opt_lines)

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

    def _generate_preview_tree_content_preview_lines(
        self, fill, preview_line_count, preview_line_width
    ):
        """
        helper method used in ``generate_preview_tree()``


        :param fill: set prefix filling before each line
        :type fill: str
        :param preview_line_count: set maximum line count of
                *content preview* part, (excluding section heading line)
        :type preview_line_count: int
        :param preview_line_width: set maximum column width of
                *content preview* part
        :type preview_line_width: int
        :return: content lines as it will be shown in preview tree
        :rtype: list[str]
        :example:
        >>> self._generate_preview_tree_content_preview_lines('$$$', 3, 10)
        ["$$$You per", "$$$When tr", "$$$User ma"]
        """
        lines = []
        if self.content and preview_line_count:  # print content of node
            for content_line in self.content[:preview_line_count]:
                lines.append(fill + content_line[:preview_line_width])
        return lines

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
