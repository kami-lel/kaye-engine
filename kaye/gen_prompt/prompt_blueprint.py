"""
define `PromptBlueprint`
"""

import re
from datetime import datetime

import importlib.metadata
from anytree import RenderTree, PreOrderIter

from .prompt_corpus_node import ROOT_NODE_NAME

__all__ = ("PromptBlueprint",)


# types of line prefix used for __repr__() generation
CHECKED_BOX_PREFIX = "[x] "
UNCHECKED_BOX_PREFIX = "[ ] "
NO_CHECKBOX_PREFIX = "    "


class PromptBlueprint:
    """
    Represents a **prompt blueprint**, encapsulating a configurable subset of
    the prompt corpus with enable/disable control over each tree node.

    A ``PromptBlueprint`` mirrors the hierarchical structure of the prompt
    corpus, but each node can be explicitly **enabled** or **disabled**.

    Use ``__repr__()`` to generate a visual representation of the **tree**.

    Use ``__str__()`` to render a **concrete prompt** composed of nodes.
    supports 2 operational modes:

    - **detached mode**: Any node is included in the output if it is enabled,
      regardless of its parent or ancestor status.

    - else: A node appears in the output
      if **both** it and all its ancestor nodes are enabled


    :param prompt_corpus: *prompt corpus* tree root node
            which this prompt blueprint attached to
    :type prompt_corpus: PromptCorpusNode
    :param blueprint_name: display name given to the prompt
    :type blueprint_name: str, optional
    :param prompt_blueprint_text: prompt blueprint text to set nodes.
            It must be formatted identical to output of ``__repr__()``
            (with tree structure and checkboxes.)
            if ``None``:
            the created ``PromptBlueprint`` has *all* nodes **disabled**
    :type prompt_blueprint_text: str, optional
    :param detached_mode: defaults to False
    :type detached_mode: bool, optional
    """

    @classmethod
    def create_full_prompt_blueprint(
        cls, prompt_corpus, blueprint_name="full"
    ):
        """
        :param prompt_corpus: *prompt corpus* tree root node
                which this prompt blueprint attached to
        :type prompt_corpus: PromptCorpusNode
        :param prompt_blueprint_name: display name given to the prompt;
                defaults to "full"
        :type prompt_blueprint_name: str, optional
        :return: an instance of ``PromptBlueprint`` attached to the given
                ``prompt_corpus``, and with **all nodes enabled**
        :rtype: PromptBlueprint
        """
        blueprint = cls(prompt_corpus, prompt_blueprint_name=blueprint_name)
        # set all nodes
        for node in PreOrderIter(prompt_corpus):
            if node is prompt_corpus:  # skip root node
                continue

            blueprint.enabled_nodes_names.append(node.name)

        return blueprint

    @property
    def is_detached_mode(self):
        """
        :return: whether the PromptBlueprint is in **detached mode**
        :rtype: bool
        """
        return ROOT_NODE_NAME not in self.enabled_nodes_names

    def set_unset_detached_mode(self, detached_mode):
        """
        Set or unset the **detached mode** for the PromptBlueprint.

        :param detached_mode: whether to set or unset the detached mode.
        :type detached_mode: bool
        """
        if detached_mode:  # set detached mode
            # ensure "○" is absent in ``.enabled_nodes_names``
            if ROOT_NODE_NAME in self.enabled_nodes_names:
                self.enabled_nodes_names.remove(ROOT_NODE_NAME)

        else:  # unset detached mode
            # ensure "○" is present in ``.enabled_nodes_names``
            if ROOT_NODE_NAME not in self.enabled_nodes_names:
                self.enabled_nodes_names.append(ROOT_NODE_NAME)

    def __init__(
        self,
        prompt_corpus,
        prompt_blueprint_text=None,
        prompt_blueprint_name=None,
        detached_mode=False,
    ):
        self.blueprint_name = prompt_blueprint_name
        self.prompt_corpus = prompt_corpus
        self.enabled_nodes_names = []  # all nodes currently enabled

        if prompt_blueprint_text:
            self._init_populate_enabled_nodes_names(prompt_blueprint_text)
        else:
            # enable tree root node means non-detached mode
            self.set_unset_detached_mode(detached_mode)

    def _init_populate_enabled_nodes_names(self, prompt_blueprint_text):
        # fixme allow use both x&X for checked box
        lines = prompt_blueprint_text.split("\n")

        # parse detached mode
        self.set_unset_detached_mode(
            lines[0] != CHECKED_BOX_PREFIX + ROOT_NODE_NAME
        )

        # find all node names in the tree
        node_names = [node.name for node in self.prompt_corpus.descendants]

        # extract all enabled headings
        pattern = r"{}.+── (.+)".format(re.escape(CHECKED_BOX_PREFIX))
        for line in lines:
            match = re.fullmatch(pattern, line)
            if match:  # find a line start w/ checked box
                found_heading = match.group(1)
                if found_heading in node_names:
                    # ensure the found heading in present in the tree
                    self.enabled_nodes_names.append(found_heading)

    def _generate_str_recursively(self, node):
        # stop recursive if this node is not enabled
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
        Return a visual representation of the **tree**, showing:

        - tree structure
        - node name (i.e. section heading)
        - node enabled/disabled status indicated by checkboxes
        - node content preview

        Root node is named ``○``.
        If it is prefixed with unchecked checkbox ``[ ]``,
        the instance operate in *detached mode*.


        :param preview_line_count: set maximum line count of
                *content preview* part for each entry,
                (excluding section heading line)
                defaults to 3
        :type preview_line_count: int
        :param preview_line_width: set maximum column width of
                *content preview* part for each entry;
                defaults to 64.
        :type preview_line_width: int
        :return: v.s.
        :rtype: str

        :example:
        >>> tree = PromptBlueprint(...)
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
        # fixme include prompt name

        opt_lines = []

        for pre, fill, node in RenderTree(self.prompt_corpus):
            node_name = node.name
            # decide either have [x] or [ ] before node lines
            checkbox_prefix = (
                CHECKED_BOX_PREFIX
                if node_name in self.enabled_nodes_names
                else UNCHECKED_BOX_PREFIX
            )

            opt_lines.append(checkbox_prefix + pre + node_name)

            # lines for the content of node
            opt_lines.extend(
                node.generate_repr_content_part(
                    NO_CHECKBOX_PREFIX + fill,
                    preview_line_count,
                    preview_line_width,
                )
            )

        return "\n".join(opt_lines)

    def __str__(self, *, hide_comment=False):
        """
        :param hide_comment: Disable placing comment part after last line;
                Defaults to False
        :type hide_comment: bool, optional
        :return: **concrete prompt** composed of nodes heading and content,
                depending on *detached mode* and each nodes' enabling status.
                Q.v. ``PromptBlueprint``
        :rtype: str
        :example:
        >>> tree = PromptBlueprint(...)
        >>> str(tree)
        # Main Title
        Overview of the methodologies used.
        ### Data Collection
        How data was gathered for analysis.
        ## Conclusion
        Summarizing the findings and implications.
        """

        # bug this will remove all blank lines, sometimes empty lines are needed
        lines = (
            self._generate_str_recursively_detached_mode(self.prompt_corpus)
            if self.is_detached_mode
            else self._generate_str_recursively(self.prompt_corpus)
        )

        # create comment part
        if not hide_comment:
            kaye_version = importlib.metadata.version("kaye")

            # append render date-time in version for alpha releases
            if "a" in kaye_version:
                kaye_version += datetime.now().strftime(".0%Y%m%d%H%M%S")

            comment_line = "<!-- {}Kaye v{} -->".format(
                (
                    "blueprint:{}; ".format(self.blueprint_name)
                    if self.blueprint_name
                    else ""
                ),
                kaye_version,
            )
            lines.append(comment_line)

        return "\n".join(lines)
