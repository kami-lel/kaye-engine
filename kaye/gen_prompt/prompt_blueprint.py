"""
define `PromptBlueprint`
"""

# TODO when generating prompts, respect empty line before headings
# Todo use kamilog


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

    Use ``.generate_preview_tree()`` (or ``__repr__()``) to generate
    a visual representation of the **tree**
    showing enabled node with ``[x]`` and disabled node with ``[ ]``

    Use ``.generate_prompt()`` (or ``__str__()``) to render
    a **concrete prompt** composed of all enabled nodes


    :param prompt_corpus: *prompt corpus* tree **root** node
            which this prompt blueprint attached to
    :type prompt_corpus: PromptCorpusNode
    :param blueprint_text: prompt blueprint text to set nodes,
            must in the same format of output of ``__repr__()``
            (with tree structure and checkboxes;)
            if ``None``: create an **empty** prompt blueprint,
            i.e. all nodes disabled
    :type blueprint_text: str
    :param blueprint_display_name: display name given to the prompt,
            defaults to ""
    :type blueprint_display_name: str, optional
    """

    def __init__(
        self,
        prompt_corpus,
        blueprint_text=None,
        *,
        blueprint_display_name="",
    ):
        self.display_name = blueprint_display_name
        self.prompt_corpus = prompt_corpus

        # list of all enabled nodes
        # each node represented by its .get_path_names()
        self.enabled = []  # default as empty blueprint

        if blueprint_text:
            self._init_populate_enabled_by_blueprint_text(blueprint_text)

    def _init_populate_enabled_by_blueprint_text(self, blueprint_text):
        """
        helper method used in ``__init__()``

        populate ``self.enabled`` by parsing the init param ``blueprint_text``
        """
        lines = blueprint_text.split("\n")

        path_hash2node = {
            hash(tuple(node.get_path())): node
            for node in self.prompt_corpus.descendants
        }

        # extract all enabled headings
        # TODO


class PromptBlueprintLegacy:

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

    def generate_preview_tree(
        self,
        preview_line_count=3,
        preview_line_width=64,
        *,
        hide_comment=False,
    ):
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
        :param hide_comment: Disable placing comment part after last line;
                Defaults to False
        :type hide_comment: bool, optional
        :return: v.s.
        :rtype: str

        :example:
        >>> tree = PromptBlueprint(...)
        >>> tree.generate_preview_tree()
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
        (blueprint:conversation; Kaye v1.2.3)
        >>> tree.generate_preview_tree(preview_line_count=0, hide_comment=True)
        [x] ○
        [x] └── Project Title
        [ ]     ├── Description
        [ ]     ├── Installation
        [ ]     ├── Usage
        [ ]     ├── Contributing
        [x]     └── License
        """
        # TODO allow preview tree to ignore some nodes

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
                node.generate_preview_tree_content_part(
                    NO_CHECKBOX_PREFIX + fill,
                    preview_line_count,
                    preview_line_width,
                )
            )

        if not hide_comment:
            comment_line = "(" + self._generate_prompt_comment_content() + ")"
            opt_lines.append(comment_line)

        return "\n".join(opt_lines)

    def generate_prompt(self, *, hide_comment=False):
        """
        :param hide_comment: disable placing comment part after last line;
                defaults to False
        :type hide_comment: bool, optional
        :return: **concrete prompt** composed of nodes heading and content,
                depending on *detached mode* and each nodes' enabling status.
                Q.v. ``PromptBlueprint``
        :rtype: str
        :example:
        >>> tree = PromptBlueprint(...)
        >>> tree.generate_prompt(hide_comment=True)
        # Main Title
        Overview of the methodologies used.
        ### Data Collection
        How data was gathered for analysis.
        ## Conclusion
        Summarizing the findings and implications.
        """
        lines = (
            self._generate_str_recursively_detached_mode(self.prompt_corpus)
            if self.is_detached_mode
            else self._generate_str_recursively(self.prompt_corpus)
        )

        # create comment part
        if not hide_comment:
            comment_line = (
                "<!-- " + self._generate_prompt_comment_content() + " -->"
            )
            lines.append(comment_line)

        return "\n".join(lines)

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

    def _generate_prompt_comment_content(self):
        """
        :return: prompt comment (used in __repr__() and __str__()) containing
                blueprint name and Kaye version
        :rtype: str

        :example:
        >>> print(tree._generate_prompt_comment_content())
        'blueprint:conversation; Kaye v1.2.3'
        """
        kaye_version = importlib.metadata.version("kaye")

        # append render date-time in version for alpha releases
        if "a" in kaye_version:
            kaye_version += datetime.now().strftime(".0%Y%m%d%H%M%S")

        return "{}Kaye v{}".format(
            (
                "blueprint:{}; ".format(self.blueprint_name)
                if self.blueprint_name
                else ""
            ),
            kaye_version,
        )

    def __repr__(self):
        return self.generate_preview_tree()

    def __str__(self):
        return self.generate_prompt()
