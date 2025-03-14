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
        cleanup = re.sub(r"\n+", "\n", full_prompt)
        # remove all empty lines
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

    def _children_as_anytree_node(self):
        """
        :return: all children of ``self`` converted to ``anytree.Node``
        :rtype: list(anytree.Node)
        """
        children_nodes = []
        # BUG

        return Node()

    def __repr__(self):
        # BUG
        self_node = Node()
        return super().__repr__()
