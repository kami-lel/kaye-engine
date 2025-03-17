"""
define ``FullPromptParserNode``
"""

import re

from anytree import Node as AnytreeNode, RenderTree

HEADING_MARKER = "#"
TREE_ROOT_NAME = "○"

__all__ = ("FullPromptParserNode",)


class FullPromptParserNode(AnytreeNode):
    """
    Represents a single node in a **Full Prompt Tree**, which is a
    structured representation of a Full Prompt. In this tree
    structure, each node organizes and categorizes content within
    a prompt, allowing for both root nodes that encompass the
    entire document and subsections identified by headings.

    :param name: name / heading of the node
    :type name: str
    :param parent: parent node in the tree structure;
    `None` for the root node.
    :type parent: FullPromptParserNode
    :param text_lines: content to be parsed, each ``str`` represents a line
    :type text_lines: list(str)
    """

    @classmethod
    def parse(cls, full_prompt):
        """
        Parses a full prompt string into a structured **Full Prompt Tree**.

        This method takes a full prompt as input,,
        and constructs the root node of the tree.
        The resulting tree structure contains nodes that
        represent the various sections and subsections of the
        prompt based on headings.

        :param full_prompt: The entire prompt to be parsed into a tree structure.
        :type full_prompt: str
        :return: The root node of the **Full Prompt Tree**,
                representing the parsed structure of the full prompt.
        :rtype: FullPromptParserNode
        """

        text_lines = cls._convert_full_prompt2lines(full_prompt)
        root = cls(TREE_ROOT_NAME, None, text_lines)
        return root

    def __init__(self, name, parent, text_lines):
        super().__init__(name, parent)
        self.content = []
        self._populate_self_by_text_lines(text_lines)

    @staticmethod
    def _convert_full_prompt2lines(full_prompt):
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
            FullPromptParserNode(heading_content, self, children_nodes)

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
        """
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
