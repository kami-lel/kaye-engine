"""
define ``PromptCorpusNode``
"""

import re

from anytree import Node as AnytreeNode, RenderTree

HEADING_MARKER = "#"
TREE_ROOT_NAME = "○"

__all__ = ("PromptCorpusNode",)


class PromptCorpusNode(AnytreeNode):
    """
    A ``PromptCorpusNode`` represents a single node in the *prompt corpus*.

    The **prompt corpus** comprises the complete set of available prompts.

    This class enables the creation of a **tree-structured** representation
    of the *prompt corpus*. Each instance of the class is a node in the tree,
    corresponding to a part of the corpus and associated with a specific
    section heading.


    :param name: section heading of the node
    :type name: str
    :param parent: parent node in the tree structure;
    `None` if the root node
    :type parent: PromptCorpusNode
    :param text_lines: content to be parsed, each ``str`` represents a line
    :type text_lines: list(str)
    """

    @classmethod
    def parse(cls, prompt_corpus_text):
        """
        Parse *prompt corpus* text into the tree structure.

        :param prompt_corpus_text: full source *prompt corpus* content
        :type prompt_corpus_text: str
        :return: **root node** of the parsed *prompt corpus* tree structure
        :rtype: PromptCorpusNode
        """

        text_lines = cls._convert_corpus_text2lines(prompt_corpus_text)
        root = cls(TREE_ROOT_NAME, None, text_lines)
        return root

    def __init__(self, name, parent, text_lines):
        super().__init__(name, parent)
        self.content = []
        self._populate_self_by_text_lines(text_lines)

    @staticmethod
    def _convert_corpus_text2lines(full_prompt):
        # remove all empty lines
        cleanup = re.sub(r"\n+(?=\Z)", "", re.sub(r"\n+", "\n", full_prompt))
        return list(cleanup.split("\n"))

    def _populate_self_by_text_lines(self, text_lines):
        # find every sub-section heading lines
        heading_prefix = HEADING_MARKER * (self.depth + 1) + " "
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

    def generate_heading_and_content_lines(self):
        """
        Generate lines representing the heading and content of the node.

        This method constructs a list of strings, where each string is a line
        representing the node's heading followed by its content. The heading
        is formatted based on the node's depth, and each content line is
        included in the resulting list.

        :return: A list of strings, each representing a line of the node's
                heading and content. The first line is the heading,
                followed by the content lines if available.
        :rtype: list[str]

        :example:
        >>> node = ...
        >>> node.generate_heading_and_content_lines()
        ['### Node Heading', 'content 1st line', 'content 2nd line']
        """
        # FIXME better docstring
        lines = []
        lines.append(HEADING_MARKER * self.depth + " " + self.name)
        lines.extend(self.content)
        return lines

    def generate_repr_content_part(
        self, fill, preview_line_count, preview_line_width
    ):
        """
        Generate a part of the string representation for the content of the node.

        This method is used to generate a portion of the result for the
        __repr__() method, allowing a preview of the node's content.

        :param fill: The string to prepend to each line of content.
        :type fill: str
        :param preview_line_count: The number of lines to include in the preview.
        :type preview_line_count: int
        :param preview_line_width: The maximum width of each preview line.
        :type preview_line_width: int
        :return: A list of formatted content lines for the node's representation.
        :rtype: list[str]
        """
        # FIXME better docstring
        lines = []
        if self.content and preview_line_count:  # print content of node
            for content_line in self.content[:preview_line_count]:
                lines.append(fill + content_line[:preview_line_width])
        return lines

    def __repr__(self, preview_line_count=3, preview_line_width=64):
        """
        Returns a string representation of the FullPromptParserNode and
        its children in a human-readable format, allowing a preview of its
        content.

        The representation includes the names of nodes in the tree as well as
        a limited preview of their respective lines of content.

        :param preview_line_count: The number of lines to preview for the
                content of the node; defaults to 3.
        :type preview_line_count: int
        :param preview_line_width: The width of each preview line,
                which determines how many characters from the content will be
                included in the preview; defaults to 64.
        :type preview_line_width: int
        :return: A string representation of the current node and its children.
        :rtype: str

        :example:
        >>> repr(tree)
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
        >>> tree.__repr__(preview_line_count=0)
        ○
        └── Project Title
            ├── Description
            ├── Installation
            ├── Usage
            ├── Contributing
            └── License
        """
        # FIXME better docstring
        opt_lines = []

        for pre, fill, node in RenderTree(self):
            # line for the node
            opt_lines.append(pre + node.name)
            # lines for the content of node
            opt_lines.extend(
                node.generate_repr_content_part(
                    fill, preview_line_count, preview_line_width
                )
            )

        return "\n".join(opt_lines)
