"""
define `PromptBlueprint`
"""

import re
from datetime import datetime

import importlib.metadata
from anytree import RenderTree, PreOrderIter, Node
from anytree.render import ContStyle

from .. import kamilog, PROGRAM_NAME
from .prompt_corpus_node import HEADING_PREFIX

__all__ = ("PromptBlueprint",)

logger = kamilog.getLogger(PROGRAM_NAME)


class PromptBlueprint(dict):
    """
    TODO summary

    :param prompt_corpus: *prompt corpus tree* **root** node
            which this prompt blueprint attached to
    :type prompt_corpus: PromptCorpusNode
    :param blueprint_display_name: display name given to the blueprint
    :type blueprint_display_name: str, optional
    :return: an instance of ``PromptBlueprint`` attached to the given
            ``prompt_corpus``, and with **all nodes checkmarked**
    """

    @classmethod
    def parse_blueprint(
        cls,
        prompt_corpus,
        blueprint_text=None,
        *,
        display_name="",
        disable_prune=False,
    ):
        """
        TODO, disable_prune


        :param prompt_corpus:
        :type prompt_corpus: PromptCorpusNode
        :param blueprint_text: prompt blueprint text to set nodes,
                must in the same format of output of ``__repr__()``
                (with tree structure and checkboxes;)
                if ``None``: create an **empty** prompt blueprint,
                i.e. all nodes disabled
        :type blueprint_text: str
        :param display_name:
        :type display_name: str, optional
        """
        # BUG need test
        bp = PromptBlueprint(prompt_corpus, display_name=display_name)
        path2node_hash = {
            node.names_path: hash(node) for node in bp.corpus.descendants
        }

        # extract all headings  ++++++++++++++++++++++++++++++++++++++++++++++++
        previous_level = -1
        previous_path = []
        for line in blueprint_text.split("\n"):
            match = re.fullmatch(cls.HEADING_LINE_PATTERN, line)

            if not match:
                continue  # skip line that is not a node heading

            is_checkmarked = match.group(1) == "x"
            level = len(match.group(2)) // 4
            heading = match.group(3)

            # dynamically decide path  -----------------------------------------
            if level > previous_level:

                if level - previous_level > 1:
                    # BUG need test & improve wording
                    logger.error(
                        "detect bad blueprint tree format at:\n%s", line
                    )
                    continue

                path = previous_path + [""]

            elif level == previous_level:
                path = previous_path

            else:
                path = previous_path[: level + 1]

            path[level] = heading
            path_tuple = tuple(path)

            # check node's existence in tree  ----------------------------------
            if path_tuple not in path2node_hash:
                # BUG need test & improve wording
                logger.warning(
                    "not part of the provided prompt corpus, skipped"
                    " during blueprint parsing:\n%s",
                    line,
                )
                continue  # skip this node

            # append a node  ---------------------------------------------------
            node_hash = path2node_hash[path_tuple]
            bp[node_hash] = is_checkmarked

            # update loop vars  ------------------------------------------------
            previous_level, previous_path = level, path

        return bp

    @classmethod
    def create_full_blueprint(cls, prompt_corpus, *, display_name="full"):
        """
        :param prompt_corpus:
        :type prompt_corpus: PromptCorpusNode
        :param display_name:
        :type display_name: str, optional
        :return: a blueprint of ``prompt_corpus`` with all nodes checkmarked
        :rtype: PromptBlueprint
        """
        # BUG need test
        blueprint = PromptBlueprint(prompt_corpus, display_name=display_name)
        # include all nodes
        for node in PreOrderIter(prompt_corpus):
            if node.parent is None:  # skip root node
                key = hash(node)
                blueprint[key] = True  #  check all nodes

        return blueprint

    @classmethod
    def create_empty_blueprint(
        cls, prompt_corpus, *, display_name="empty", disable_prune=False
    ):
        """
        :param prompt_corpus:
        :type prompt_corpus: PromptCorpusNode
        :param display_name:
        :type display_name: str, optional
        :return: a blueprint of ``prompt_corpus`` with none of nodes checkmarked
        :rtype: PromptBlueprint
        """
        # BUG need test
        if disable_prune:
            bp = cls.create_full_blueprint(
                prompt_corpus, display_name=display_name
            )
            for k in bp:  # un-checkmark all node
                bp[k] = False
            return bp
        else:
            return PromptBlueprint(prompt_corpus, display_name=display_name)

    def prune(self):
        pass  # TODO

    def generate_preview_tree(
        self,
        *,
        show_full_tree=False,
        preview_line_count=3,
        preview_line_width=64,
        hide_comment=False,
    ):
        pass  # TODO

    def generate_prompt(self, *, hide_comment=False):
        pass  # TODO

    HEADING_LINE_PATTERN = r"\[([x ])\] (.*)[└├]── (.+)"

    def __init__(self, prompt_corpus, *, display_name=""):
        # BUG need test
        super().__init__()  # init as empty dict
        self.corpus = prompt_corpus
        self.display_name = display_name

    def __repr__(self):
        # BUG need test
        return "PromptBlueprint({})".format(self.display_name)

    def __str__(self):
        # BUG need test
        return self.generate_preview_tree()


class PromptBlueprintOld:  # HACK rm

    def __init__(
        self,
        prompt_corpus,
        blueprint_text=None,
        *,
        display_name="",
    ):
        self.display_name = display_name
        self.prompt_corpus = prompt_corpus

        # list of all enabled nodes
        self.enabled = []  # default as empty blueprint

        if blueprint_text:
            self._init_populate_enabled_by_blueprint_text(blueprint_text)

    def generate_preview_tree(
        self,
        *,
        show_full_tree=False,
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


        :param show_full_tree: _description_, defaults to False
        :type show_full_tree: bool, optional
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
            ○
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
            ○
        [x] └── Project Title
        [ ]     ├── Description
        [ ]     ├── Installation
        [ ]     ├── Usage
        [ ]     ├── Contributing
        [x]     └── License
        """

        preview_tree = self._PreviewTreeNode(self, self.prompt_corpus, None)

        if not show_full_tree:
            preview_tree.prune_trivial_branches()

        opt_lines = []
        for pre, fill, node in RenderTree(preview_tree, style=ContStyle()):
            if node.parent is None:
                root_line = "    {}".format(node.name)
                opt_lines.append(root_line)
                continue

            # create node / heading line
            checkbox = "[x] " if node.is_enabled() else "[ ] "
            heading_line = checkbox + pre + node.name
            opt_lines.append(heading_line)

            # generate content preview
            opt_lines.extend(
                node.concurrent_corpus_node.generate_preview_tree_content_part(
                    "    " + fill, preview_line_count, preview_line_width
                )
            )

        # append comment line
        if not hide_comment:
            comment_line = "({})".format(self._generate_comment_content())
            opt_lines.append(comment_line)

        return "\n".join(opt_lines)

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
        # generate lines from root node
        lines = self._generate_prompt_recursively(self.prompt_corpus)

        # create comment part
        if not hide_comment:
            comment_line = "<!-- " + self._generate_comment_content() + " -->"
            lines.append(comment_line)

        return "\n".join(lines)

    class _PreviewTreeNode(Node):
        """
        helper class used
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

        def is_enabled(self):
            """
            :return: whether this node is enabled in the blueprint;
            :rtype: bool
            """
            # TODO opmz by hash names_path
            names_path = self.concurrent_corpus_node.names_path
            return any(
                (names_path == node.names_path)
                for node in self.blueprint.enabled
            )

        def prune_trivial_branches(self):
            """
            prune all branches that contains no enabled nodes

            :return: whether this node has any enabled descendants
            :rtype: bool
            """
            if self.is_leaf:
                if self.is_enabled():
                    return True  # keep this enabled leaf node
            else:
                non_trivial = [
                    child.prune_trivial_branches() for child in self.children
                ]
                if self.is_enabled() or any(non_trivial):
                    return True  # self is marked/children has marked nodes

            # remove self from tree, ready for garbage collection
            self.parent = None
            return False

    def __init__(self, blueprint, concurrent_corpus_node, parent):
        super().__init__(concurrent_corpus_node.name, parent)

        self.blueprint = blueprint
        self.concurrent_corpus_node = concurrent_corpus_node

        # create children nodes
        for child_concurrent_node in concurrent_corpus_node.children:
            _PreviewTreeNode(blueprint, child_concurrent_node, self)

    def _generate_prompt_recursively(self, node):
        """
        helper method used in ``.generate_preview()``

        generate recursively prompt lines from ``node``
        """
        lines = []

        try:
            idx = self.enabled.index(node)
        except ValueError:
            idx = -1
        if idx >= 0 and node.parent is not None:
            level = node.depth

            # add empty lines before headings
            if idx > 0:
                lines.append("")

            # add heading line
            heading_line = HEADING_PREFIX * level + " " + node.name
            lines.append(heading_line)
            # add content lines
            lines.extend(node.content)

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
