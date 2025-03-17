"""
define `PromptTemplate`
"""

from anytree import RenderTree

from .full_prompt_parser import TREE_ROOT_NAME
from .current_full_prompt_tree import get_current_full_prompt_tree

__all__ = ("PromptTemplate",)

CHECKED_BOX = "[x]"
UNCHECKED_BOX = "[ ]"
NO_CHECKBOX = "   "


class PromptTemplate:

    def __init__(
        self,
        savable_prompt_template=None,
        detached_mode=False,
        full_prompt_tree=None,
    ):
        self.enabled_nodes_names = []
        # enable tree root node means non-detached mode
        if not detached_mode:
            self.enabled_nodes_names.append(TREE_ROOT_NAME)

        self.full_prompt_tree = (
            full_prompt_tree or get_current_full_prompt_tree()
        )

        if savable_prompt_template:
            self._init_populate_enabled_nodes_names(savable_prompt_template)

    def _init_populate_enabled_nodes_names(self, savable_prompt_template):
        pass  # TODO

    def __repr__(self, preview_line_count=3, preview_line_width=64):
        """
        Returns a string representation of the PromptTemplate and its
        enabled nodes in a human-readable format, allowing a preview of
        each node's content.

        The representation includes checkbox indicators for whether each
        node is enabled (checked or unchecked) along with the respective
        lines of content previewed according to the specified parameters.

        :param preview_line_count: The number of lines to preview for the
                content of the node; defaults to 3.
        :type preview_line_count: int
        :param preview_line_width: The width of each preview line,
               which determines how many characters from the content will be
               included in the preview; defaults to 64.
        :type preview_line_width: int
        :return: A string representation of the current node, with enabled
               nodes and their content previews included.
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

    def __str__(self, preview_line_count=3, preview_line_width=64):
        # TODO docstring
        return ""
