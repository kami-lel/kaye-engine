"""
define `PromptTemplate`
"""

import re
from anytree import RenderTree

from .full_prompt_parser import TREE_ROOT_NAME
from .current_full_prompt_tree import get_current_full_prompt_tree

__all__ = ("PromptTemplate",)

CHECKED_BOX = "[x] "
UNCHECKED_BOX = "[ ] "
NO_CHECKBOX = "    "


class PromptTemplate:
    """
    A ``PromptTemplate`` represents a part or the entirety of
    a *Full Prompt Tree*. It allows nodes in the tree to be enabled or disabled,
    controlling which prompts are extracted and displayed from
    the full prompt tree.

    Use ``__repr__`` to obtain a representation of the attached
    full prompt tree, along with the enabled/disabled status of each node.

    You may provide a ``savable_prompt_template`` during creation; it must be
    formatted like the output of the repr. This will set the enabled/disabled
    status during the initialization of the template.

    Use ``__str__`` to render the content of the prompt based on the
    enabled/disabled conditions of the tree.

    If in *detached_mode*, the prompt allows disconnected individual nodes
    regardless of the tree structure. For instance, leaf nodes may be enabled
    without requiring their root to be enabled. Conversely, if not in detached
    mode, a node is rendered only when it is enabled and all its ancestors are
    also enabled.

    :param savable_prompt_template: string representation of a
            prompt template, defaults to None.
    :type savable_prompt_template: str, optional
    :param detached_mode: A flag indicating whether to enable detached mode
            for the PromptTemplate, defaults to False.
    :type detached_mode: bool, optional
    :param full_prompt_tree: An optional FullPromptParserNode instance that
            represents the full prompt tree. Defaults to None.
    :type full_prompt_tree: FullPromptParserNode, optional
    """

    @property
    def is_detached_mode(self):
        """
        :return: whether the PromptTemplate is in **detached mode**
        :rtype: bool
        """
        return TREE_ROOT_NAME not in self.enabled_nodes_names

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
        # fixme allow use both x&X for checekd box
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

    def _generate_str_recursively(self, node):
        # stop recurisve if this node is not enabled
        if node.name not in self.enabled_nodes_names:
            return []

        lines = []
        if node.parent is not None:  # skip root node
            lines.extend(node.generate_heading_and_content_lines())

        # children
        for child_node in node.children:
            lines.extend(self._generate_str_recursively(child_node))

        return lines

    def _generate_str_recursively_detached_mode(self, node):
        lines = []

        if node.name in self.enabled_nodes_names and node.parent is not None:
            lines.extend(node.generate_heading_and_content_lines())

        # children
        for child_node in node.children:
            lines.extend(
                self._generate_str_recursively_detached_mode(child_node)
            )

        return lines

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

        :example:
        >>> repr(tree)
        [x] ○
        [x] └── Project Title
        [ ]     ├── Description
                │   A brief overview of the project, its purpose, and goals.
        [ ]     ├── Installation
                │   1. Clone the repo
                │   2. Install dependencies
                │   3. Run the application
        [ ]     ├── Usage
                │   Provide instructions on how to use the application.
        [ ]     ├── Contributing
                │   1. Fork the repo
                │   2. Create a new branch
                │   3. Submit a pull request
        [x]     └── License
                    This project is licensed under the MIT License.
        >>> tree.__repr__(preview_line_count=0)
        [x] ○
        [x] └── Project Title
        [ ]     ├── Description
        [ ]     ├── Installation
        [ ]     ├── Usage
        [ ]     ├── Contributing
        [x]     └── License
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
        """
        Returns the string representation of the PromptTemplate,
        including either the full prompt or part of it based on enabled nodes.

        :return: the prompt showing enabled nodes and their respective content.
        :rtype: str

        :example:
        >>> str(tree)
        # Main Title
        Overview of the methodologies used.
        ### Data Collection
        How data was gathered for analysis.
        ## Conclusion
        Summarizing the findings and implications.
        """
        lines = (
            self._generate_str_recursively_detached_mode(self.full_prompt_tree)
            if self.is_detached_mode
            else self._generate_str_recursively(self.full_prompt_tree)
        )
        return "\n".join(lines)
