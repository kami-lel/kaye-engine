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

    def __init__(self, tree_root=None, saved_prompt_template=None):
        self.enables = [TREE_ROOT_NAME]
        self.tree_root = tree_root or get_current_full_prompt_tree()

    def __repr__(self, preview_line_count=3, preview_line_width=64):
        # TODO docstring

        opt_lines = []

        for pre, fill, node in RenderTree(self.tree_root):
            node_name = node.name
            # decide either have [x] or [ ] before node lines
            checkbox_prefix = (
                CHECKED_BOX if node_name in self.enables else UNCHECKED_BOX
            )

            opt_lines.append(checkbox_prefix + pre + node.name)

            # lines for the content of node
            opt_lines.extend(
                node.generate_repr_content_part(
                    NO_CHECKBOX + fill, preview_line_count, preview_line_width
                )
            )

        return "\n".join(opt_lines)

    def __str__(self, preview_line_count=3, preview_line_width=64):
        # TODO docstring
        opt_lines = []

        for pre, fill, node in RenderTree(self.tree_root):
            node_name = node.name
            if node_name in self.enables:
                # node heading line
                opt_lines.append(pre + node.name)

                # lines for the content of node
                opt_lines.extend(
                    node.generate_repr_content_part(
                        fill, preview_line_count, preview_line_width
                    )
                )

        return "\n".join(opt_lines)
