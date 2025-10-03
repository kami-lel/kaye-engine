"""
define `PromptBlueprint`
"""

# Todo use kamilog


import re
from datetime import datetime

import importlib.metadata
from anytree import RenderTree, PreOrderIter, Node
from anytree.render import ContStyle

from .prompt_corpus_node import ROOT_NODE_NAME

__all__ = ("PromptBlueprint",)


class _PreviewTreeNode(Node):
    """
    helper class usedVjj
    in ``.generate_preview_tree()`` of ``class PromptBlueprint``

    create a tree structured same as prompt corpus tree
    for the utility of preview tree generation


    :param blueprint: blueprint object which create this preview tree
    :type blueprint: PromptBlueprint
    :param concurrent_corpus_node: concurrent node in the prompt corpus tree
    :type concurrent_corpus_node: PromptCorpusNode
    :param parent:
    :type parent: _PreviewTreeNode
    """

    def get_prefix_content(self):
        """
        :return: '[x] ' if this node is enabled in the blueprint;
                '[ ] ' otherwise
        :rtype: str
        """
        return (
            "[x] "
            if (
                self.concurrent_corpus_node.names_path
                in self.blueprint.enabled
            )
            else "[ ] "
        )

    def generate_preview_content_lines(
        self, fill, preview_line_count, preview_line_width
    ):
        return []  # TODO

    # HACK
    # def generate_preview_tree_content_part(
    #     self, fill, preview_line_count, preview_line_width
    # ):
    #     """
    #     :param fill: set prefix filling before each line
    #     :type fill: str
    #     :param preview_line_count: set maximum line count of
    #             *content preview* part, (excluding section heading line)
    #     :type preview_line_count: int
    #     :param preview_line_width: set maximum column width of
    #             *content preview* part
    #     :type preview_line_width: int
    #     :return: content lines of ``self`` as it will be shown in
    #             tree ``__repr__()``, with formatting included
    #             Each entry represent a line in the ``__repr__()``
    #     :rtype: list[str]
    #     :example:
    #     >>> node.generate_preview_tree_content_part('$$$' 3, 10)
    #     ["$$$You per", "$$$When tr", "$$$User ma"]
    #     """
    #     lines = []
    #     if self.content and preview_line_count:  # print content of node
    #         for content_line in self.content[:preview_line_count]:
    #             lines.append(fill + content_line[:preview_line_width])
    #     return lines

    def __init__(self, blueprint, concurrent_corpus_node, parent):
        super().__init__(concurrent_corpus_node.name, parent)

        self.blueprint = blueprint
        self.concurrent_corpus_node = concurrent_corpus_node

        # create children nodes
        for child_concurrent_node in concurrent_corpus_node.children:
            _PreviewTreeNode(blueprint, child_concurrent_node, self)


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

    @classmethod
    def create_full_prompt_blueprint(
        cls, prompt_corpus, blueprint_display_name="full"
    ):
        """
        :param prompt_corpus: *prompt corpus* tree root node
                which this prompt blueprint attached to
        :type prompt_corpus: PromptCorpusNode
        :param blueprint_display_name: display name given to the prompt;
                defaults to "full"
        :type blueprint_display_name: str, optional
        :return: an instance of ``PromptBlueprint`` attached to the given
                ``prompt_corpus``, and with **all nodes enabled**
        :rtype: PromptBlueprint
        """
        # TODO need tests
        blueprint = cls(
            prompt_corpus, blueprint_display_name=blueprint_display_name
        )
        # set all nodes
        for node in PreOrderIter(prompt_corpus):
            if node is prompt_corpus:  # skip root node
                continue

            blueprint.enabled.append(node)

        return blueprint

    def generate_preview_tree(
        self,
        *,
        enable_full_tree=False,
        preview_line_count=3,
        preview_line_width=64,
        hide_comment=False,
    ):
        """
        generate a visual representation of the **tree**, showing:

        - tree structure
        - node name (i.e. section heading)
        - node enabled/disabled status, prefixed with:

          - ``[x]`` for enabled node
          - ``[ ]`` for disabled node

        - node content preview


        :param enable_full_tree: _description_, defaults to False
        :type enable_full_tree: bool, optional
        :param preview_line_count: set maximum line count of
                *content preview* part for each entry,
                (excluding section heading line;)
                defaults to 3
        :type preview_line_count: int, optional
        :param preview_line_width: set maximum column width of
                *content preview* part for each entry;
                defaults to 64
        :type preview_line_count: int, optional
        :param hide_comment: disable comment part after last line;
                defaults to False
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

        preview_tree = _PreviewTreeNode(self, self.prompt_corpus, None)

        # TODO del irrelevant nodes

        opt_lines = []
        for pre, fill, node in RenderTree(preview_tree, style=ContStyle()):
            # create node / heading line
            heading_line = node.get_prefix_content() + pre + node.name
            opt_lines.append(heading_line)

            # preview lines
            opt_lines.extend(
                node.generate_preview_content_lines(
                    fill, preview_line_count, preview_line_width
                )
            )

        # append comment line
        if not hide_comment:
            comment_line = "({})".format(self._generate_comment_content())
            opt_lines.append(comment_line)

        return "\n".join(opt_lines)

        # HACK
        # for pre, fill, node in RenderTree(self.prompt_corpus):
        #     node_name = node.name
        #     # decide either have [x] or [ ] before node lines
        #     checkbox_prefix = (
        #         CHECKED_BOX_PREFIX
        #         if node_name in self.enabled_nodes_names
        #         else UNCHECKED_BOX_PREFIX
        #     )

        #     opt_lines.append(checkbox_prefix + pre + node_name)

        #     # lines for the content of node
        #     opt_lines.extend(
        #         node.generate_preview_tree_content_part(
        #             NO_CHECKBOX_PREFIX + fill,
        #             preview_line_count,
        #             preview_line_width,
        #         )
        #     )

    def generate_prompt(self, *, hide_comment=False):
        """
        :param hide_comment: disable comment part after last line;
                defaults to False
        :type hide_comment: bool, optional
        :return: **concrete prompt** composed of nodes heading and content
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
        # TODO need tests
        # generate lines from root node
        lines = self._generate_prompt_recursively(self.prompt_corpus)

        # create comment part
        if not hide_comment:
            comment_line = "<!-- " + self._generate_comment_content() + " -->"
            lines.append(comment_line)

        return "\n".join(lines)

    HEADING_LINE_PATTERN = r"\[([x ])\] (.*)[└├]──(.+) "

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
        self.enabled = []  # default as empty blueprint

        if blueprint_text:
            self._init_populate_enabled_by_blueprint_text(blueprint_text)

    def _init_populate_enabled_by_blueprint_text(self, blueprint_text):
        """
        helper method used in ``__init__()``

        populate ``self.enabled`` by parsing the init param ``blueprint_text``
        """
        # TODO need tests
        lines = blueprint_text.split("\n")

        path_hash2node = {
            hash(tuple(node.get_path())): node
            for node in self.prompt_corpus.descendants
        }

        # extract all enabled headings
        path = []
        for line in lines:
            match = re.fullmatch(self.HEADING_LINE_PATTERN, line)
            if match:  # find all heading lines in the tree
                is_checked = bool(match.group(1))
                level = len(match.group(2)) // 4
                heading = match.group(3)

                path[level] = heading
                path_hash = hash(tuple(path))
                if path_hash not in path_hash2node:
                    # Fixme better wording, use logger
                    raise ValueError

                if is_checked:
                    node = path_hash2node[path_hash]
                    self.enabled.append(node)

    def _generate_prompt_recursively(self, node):
        """
        helper method used in ``.generate_preview()``

        generate recursively prompt lines from ``node``
        """
        lines = []

        # BUG when generating prompts, respect empty line before headings
        if node in self.enabled and node.parent is not None:
            lines.extend(node.generate_heading_and_content_lines())

        # children
        for child_node in node.children:
            lines.extend(self._generate_prompt_recursively(child_node))

        return lines

    def _generate_comment_content(self):
        """
        helper method used in ``.generate_preview_tree()`` and
        ``.generate_prompt()``


        :return: prompt comment containing blueprint name and Kaye version
        :rtype: str
        :example:
        >>> print(tree._generate_prompt_comment_content())
        'blueprint: chat; Kaye v1.2.3'
        """
        kaye_version = importlib.metadata.version("kaye")

        # append render date-time in version for alpha releases
        if "a" in kaye_version:
            kaye_version += datetime.now().strftime(".0%Y%m%d%H%M%S")

        name_part = (
            "blueprint: {}; ".format(self.display_name)
            if self.display_name
            else ""
        )

        return "{}Kaye v{}".format(name_part, kaye_version)

    def __repr__(self):
        return self.generate_preview_tree()

    def __str__(self):
        return self.generate_prompt()
