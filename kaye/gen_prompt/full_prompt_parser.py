"""
define ``FullPromptParserNode``
"""

import re
from collections import OrderedDict

from anytree import Node, RenderTree

HEADING_MARKER = "#"

__all__ = ("FullPromptParserNode",)


class FullPromptParserNode(OrderedDict):
    """
    Represents a single node in a **Full Prompt Tree**, which is a
    structured representation of a Full Prompt. In this tree
    structure, each node organizes and categorizes content within
    a prompt, allowing for both root nodes that encompass the
    entire document and subsections identified by headings.

    :param text:
    :type text: str or list(str)
    :param level: The hierarchical level of this node within the tree structure:

    - ``0`` for the root node (the entire document)
    - ``1`` for first-level sections (e.g., a section
    under a single `# heading`)
    - etc.

    :type level: int, optional
    :param parent: parent node in the tree structure;
    `None` for the root node.
    :type parent: FullPromptTreeNode
    """

    def __new__(cls, text, parent=None):
        return super().__new__(cls, {})  # new as an empty dict

    def __init__(self, text, parent=None):
        self.parent = parent
        self.content = ""

        if parent is None:  # when current node is root
            self.level = 0
            text = self._convert_full_prompt2str_list_per_line(text)
        else:
            self.level = parent.level + 1

        self._populate_self_by_str_line(text)

    @staticmethod
    def _convert_full_prompt2str_list_per_line(full_prompt):
        # remove all empty lines
        cleanup = re.sub(r"\n+(?=\Z)", "", re.sub(r"\n+", "\n", full_prompt))
        return list(cleanup.split("\n"))

    def _populate_self_by_str_line(self, lines):
        heading_prefix = HEADING_MARKER * (self.level + 1) + " "

        # find every sub-section heading lines
        heading_lines = []
        for idx, line in enumerate(lines):
            if line.startswith(heading_prefix):
                heading_lines.append(idx)

        if not heading_lines:  # contain no subsection
            self.content = "\n".join(lines)  # all lines are content
            return

        # this node contains subsections
        # parse the content part out
        self.content = "\n".join(lines[: heading_lines[0]])

        # parse sub-sections as nodes
        heading_lines.append(len(lines))
        for start, end in zip(heading_lines, heading_lines[1:]):
            # extract heading content
            # e.g. "### this is heading " -> "this is heading"
            heading_content = lines[start][len(heading_prefix) :].strip()
            self[heading_content] = FullPromptParserNode(
                lines[start + 1 : end], self
            )

    def as_anytree_node(
        self,
        node_name=None,
        parent=None,
        preview_line_count=3,
        preview_line_width=64,
    ):
        """
        Convert the current node and its children into an
        `anytree.Node`.

        (helper method used in ``__repr__()``)

        :param node_name: Tag or name of the current node;
                `None` if the node is root.
        :type node_name: str; NoneType
        :param parent: The parent node in the tree structure.
        :type parent: anytree.Node; NoneType
        :param preview_line_count: The number of lines to preview for the
                content of the node; defaults to 3.
        :type preview_line_count: int
        :param preview_line_width: The width of each preview line,
                which determines how many characters from the content
                will be included in the preview; defaults to 64.
        :type preview_line_width: int
        :return: A node representing the current node and its children.
        :rtype: anytree.Node
        """

        if node_name is None:
            node_name = "○"

        if self.content and preview_line_count:
            # convert self.content into lines required by anytree node
            lines = [
                line[:preview_line_width] for line in self.content.split("\n")
            ][:preview_line_count]
        else:
            lines = []

        at_node = Node(node_name, parent=parent, lines=lines)

        # make childrens connected to self
        for key, value in self.items():
            value.as_anytree_node(
                key, at_node, preview_line_count, preview_line_width
            )

        return at_node

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

        self_as_anytree_node = self.as_anytree_node(
            None,
            None,
            preview_line_count=preview_line_count,
            preview_line_width=preview_line_width,
        )

        for pre, fill, node in RenderTree(self_as_anytree_node):
            opt_lines.append(pre + node.name)
            for line in node.lines:
                opt_lines.append(fill + line)

        return "\n".join(opt_lines)
