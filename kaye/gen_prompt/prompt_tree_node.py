"""
Defines the `PromptTreeNode` class for creating a hierarchical
Prompt Tree structure.
"""

import re
from collections import OrderedDict

HEADING_MARKER = "#"


__all__ = ("PromptTreeNode",)


class PromptTreeNode(OrderedDict):
    """
    represents a single node in a Prompt Tree structure

    :param text:
    :type text: str or list(str)
    :param level: level which this node exist, e.g.

    - ``0`` for root node (entire document)
    - ``1`` for 1st level section, i.e. an section of ``# heading``
    - etc.

    :type level: int, optional
    :param parent: parent of the node in the tree; ``None`` if root node
    :type parent: PromptTreeNode
    """

    def __new__(cls, text, parent=None):
        return super().__new__(cls, {})  # new as empty dict

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
            self[heading_content] = PromptTreeNode(
                lines[start + 1 : end], self
            )

    def __repr__(self, indent=0, column_width_limit=79):
        opt = []

        for key, value in self.items():
            entries = []
            # title line
            entries.append(" " * indent + key)

            # content line
            content = value.content
            if content:
                content = re.sub(r"\n", "⏎", content)
                content_line = " " * (indent + 12) + content
                limited_content_line = content_line[:column_width_limit]
                entries.append(limited_content_line)

            # sub nodes
            entries.append(value.__repr__(indent + 4, column_width_limit))

            opt.append("\n".join(entries))

        return "".join(opt)
