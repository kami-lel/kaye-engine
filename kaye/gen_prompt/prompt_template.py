"""
define `PromptTemplate`
"""

import re
from anytree import RenderTree

from .full_prompt_parser import TREE_ROOT_NAME, HEADING_MARKER
from .current_full_prompt_tree import get_current_full_prompt_tree

__all__ = ("PromptTemplate",)

CHECKED_BOX = "[x]"
UNCHECKED_BOX = "[ ]"
NO_CHECKBOX = "   "


class PromptTemplate:
    """
    _summary_

    :param savable_prompt_template: _description_, defaults to None
    :type savable_prompt_template: _type_, optional
    :param detached_mode: _description_, defaults to False
    :type detached_mode: bool, optional
    :param full_prompt_tree: _description_, defaults to None
    :type full_prompt_tree: FullPromptParserNode, optional
    """

    # TODO docstring

    def __init__(
        self,
        savable_prompt_template=None,
        detached_mode=False,
        full_prompt_tree=None,
    ):
        self.enabled_nodes_names = []

        self.full_prompt_tree = (
            full_prompt_tree or get_current_full_prompt_tree()
        )

        if savable_prompt_template:
            self._init_populate_enabled_nodes_names(savable_prompt_template)
        else:
            # enable tree root node means non-detached mode
            self.set_unset_detached_mode(detached_mode)

    def _init_populate_enabled_nodes_names(self, savable_prompt_template):
        lines = savable_prompt_template.split("\n")

        # parse detached mode
        self.set_unset_detached_mode(lines[0] != CHECKED_BOX + TREE_ROOT_NAME)

        # find all node names in the tree
        node_names = [node.name for node in self.full_prompt_tree.descendants]

        # extract all enabled headings
        pattern = r"{}.+── (.+)".format(re.escape(CHECKED_BOX))
        for line in lines:
            match = re.fullmatch(pattern, line)
            if match:  # find a line start w/ checked box
                found_heading = match.group(1)
                if found_heading in node_names:
                    # ensure the found heading in present in the tree
                    self.enabled_nodes_names.append(found_heading)

    def set_unset_detached_mode(self, detached_mode):
        """
        Set or unset the **detached mode** for the PromptTemplate.

        :param detached_mode: whether to set or unset the detached mode.
        :type detached_mode: bool
        """
        if detached_mode:  # set detached mode
            # ensure "○" is absent in ``.enabled_nodes_names``
            if TREE_ROOT_NAME in self.enabled_nodes_names:
                self.enabled_nodes_names.remove(TREE_ROOT_NAME)

        else:  # unset detached mode
            # ensure "○" is present in ``.enabled_nodes_names``
            if TREE_ROOT_NAME not in self.enabled_nodes_names:
                self.enabled_nodes_names.append(TREE_ROOT_NAME)

    @property
    def is_detached_mode(self):
        """
        :return: whether the PromptTemplate is in **detached mode**
        :rtype: bool
        """
        return TREE_ROOT_NAME not in self.enabled_nodes_names

    def __repr__(self, preview_line_count=3, preview_line_width=64):
        """
        Returns a brief string representation of the PromptTemplate,
        showing enabled nodes along with a preview of their content.

        It includes checkbox indicators for enabled nodes (checked or
        unchecked) with content previews based on the provided parameters.

        :param preview_line_count: Number of lines to preview for node content.
        :type preview_line_count: int
        :param preview_line_width: Width of each preview line; defaults to 64.
        :type preview_line_width: int
        :return: String representation of current node with previews.
        :rtype: str
        """
        opt_lines = []

        for pre, fill, node in RenderTree(self.full_prompt_tree):
            node_name = node.name
            # decide either have [x] or [ ] before node lines
            checkbox_prefix = (
                CHECKED_BOX
                if node_name in self.enabled_nodes_names
                else UNCHECKED_BOX
            )

            opt_lines.append(checkbox_prefix + pre + node_name)

            # lines for the content of node
            opt_lines.extend(
                node.generate_repr_content_part(
                    NO_CHECKBOX + fill, preview_line_count, preview_line_width
                )
            )

        return "\n".join(opt_lines)

    def __str__(self):
        # TODO docstring

        lines = self._generate_str_recursively(self.full_prompt_tree)
        return "\n".join(lines)

    def _generate_str_recursively(self, node):
        node_name = node.name

        if node_name not in self.enabled_nodes_names:
            return []

        lines = []

        if node.parent is not None:  # skip root node
            # heading line
            lines.append(HEADING_MARKER * node.depth + " " + node_name)

            # contents
            lines.extend(node.content)

        # children
        for child_node in node.children:
            lines.extend(self._generate_str_recursively(child_node))

        return lines
