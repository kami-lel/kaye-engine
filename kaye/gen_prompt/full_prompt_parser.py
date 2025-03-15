"""
define ``FullPromptParserNode``
"""

import re
from collections import OrderedDict

from anytree import Node as AnytreeNode, RenderTree

HEADING_MARKER = "#"
TREE_ROOT_NAME = "○"

__all__ = ("FullPromptParserNode",)


class FullPromptParserNode(AnytreeNode):

    @classmethod
    def parse(cls, full_prompt):
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

    def __repr__(self, preview_line_count=3, preview_line_width=64):
        opt_lines = []

        for pre, fill, node in RenderTree(self):
            opt_lines.append(pre + node.name)
            if node.content and preview_line_count:  # print content of node
                for content_line in node.content[:preview_line_count]:
                    opt_lines.append(fill + content_line[:preview_line_width])

        return "\n".join(opt_lines)


# FIXME deprecation
class FullPromptParserNodeAlt(OrderedDict):
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
        pass

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
        pass
