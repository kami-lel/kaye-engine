"""
define `PromptBlueprint`
"""

import re
from datetime import datetime
from copy import copy

import importlib.metadata
from anytree import RenderTree, PreOrderIter, Node
from anytree.render import ContStyle

from .. import kamilog, PROGRAM_NAME
from .prompt_corpus_node import HEADING_PREFIX, PromptCorpusNode

__all__ = ("PromptBlueprint",)

logger = kamilog.getLogger(PROGRAM_NAME)


# constants  ###################################################################
CHECKMARKED_PREFIX = "[x] "
UNCHECKMARKED_PREFIX = "[ ] "
EMPTY_PREFIX = "    "


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
    def parse(
        cls,
        prompt_corpus,
        blueprint_text,
        *,
        display_name="",
        disable_prune=False,
    ):
        """
        parse ``blueprint_text`` into a blueprint object


        :param prompt_corpus:
        :type prompt_corpus: PromptCorpusNode
        :param blueprint_text: prompt blueprint text to set nodes, must in
                the same format of output of ``.generate_preview_tree()``
                (with tree structure and checkmarks)
        :type blueprint_text: str
        :param display_name:
        :type display_name: str, optional
        :param disable_prune: by default, the parsed tree does not include
                irreverent nodes;
                when ``disable_prune``, the parsed tree contains the full
                prompt corpus tree of ``prompt_corpus``
        :type disable_prune: bool, optional
        :return: a blueprint parsed from ``blueprint_text``
        :rtype: PromptBlueprint
        """
        bp = PromptBlueprint(prompt_corpus, display_name=display_name)
        path2node_hash = {
            node.path_of_names: hash(node) for node in bp.corpus.descendants
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
                    # Bug need test & improve wording
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
                # Bug need test & improve wording
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
        :return: a blueprint with all nodes from `prompt_corpus`,
                and checkmarking all nodes
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
    def create_empty_blueprint(cls, prompt_corpus, *, display_name="empty"):
        """
        :param prompt_corpus:
        :type prompt_corpus: PromptCorpusNode
        :param display_name:
        :type display_name: str, optional
        :return: a blueprint with all nodes from `prompt_corpus`,
                but checkmarking all nodes
        :rtype: PromptBlueprint
        """
        # BUG need test
        bp = cls.create_full_blueprint(
            prompt_corpus, display_name=display_name
        )
        for k in bp:  # un-checkmark all node
            bp[k] = False
        return bp

    def __init__(self, prompt_corpus, *, display_name=""):
        super().__init__()  # init as empty dict
        self.corpus = prompt_corpus
        self.display_name = display_name

    def generate_preview_tree(
        self,
        *,
        preview_line_count=3,
        preview_line_width=64,
        show_full_tree=False,
        hide_comment=False,
    ):
        """
        generate **preview tree** of the blueprint,
        an human-readable representation


        :param preview_line_count: set maximum line count of
                *content preview* part, (excluding section heading line);
                defaults to 3
        :type preview_line_count: int
        :param preview_line_width: set maximum column width of
                *content preview* part;
                defaults to 64.
        :type preview_line_width: int
        :param show_full_tree: whether to show the full corpus tree,
                regardless of node's inclusion in this blueprint;
        :type show_full_tree: bool, optional
        :param hide_comment: disable comment part after last line;
                defaults to False
        :type hide_comment: bool, optional
        :return: the preview tree
        :rtype: str
        """
        if show_full_tree:
            preview_tree = self.corpus
        else:
            # create a duplicated tree,
            # but contains only nodes relevant to this blueprint
            preview_tree = _create_pruned_tree_for_preview_recursively(
                self, self.corpus
            )

        # generate content  ----------------------------------------------------
        opt_lines = []
        for pre, fill, node in RenderTree(preview_tree):
            # line for tree structure
            checkmark_prefix = (
                CHECKMARKED_PREFIX if (node in self) else UNCHECKMARKED_PREFIX
            )
            if node.is_root:
                checkmark_prefix = EMPTY_PREFIX

            node_line = checkmark_prefix + pre + node.name
            opt_lines.append(node_line)

            # lines for node content preview
            content_fill = "    " + fill
            opt_lines.extend(
                # pylint: disable=protected-access
                node._generate_preview_tree_content_preview_lines(
                    content_fill, preview_line_count, preview_line_width
                )
            )

        # append comment line
        if not hide_comment:
            comment_line = "<!-- " + self._generate_comment_content() + " -->"
            opt_lines.append(comment_line)

        return "\n".join(opt_lines)

    def generate_prompt(self, *, hide_comment=False):
        """
        TODO


        :param hide_comment: disable comment part after last line;
                defaults to False
        :type hide_comment: bool, optional
        :return: **concrete prompt** composed of nodes heading and content
        :rtype: str
        """
        return ""  # TODO

    def prune(self):
        """
        :return: a **pruned** blueprint (of ``self``)
                which contains only branches with checkmarked nodes
        :rtype: PromptBlueprint
        """
        # BUG need test
        pruned_bp = PromptBlueprint(
            self.corpus, display_name=self.display_name
        )
        _add_all_unprunable_nodes_recursively(self, pruned_bp, self.corpus)
        return pruned_bp

    HEADING_LINE_PATTERN = r"\[([x ])\] (.*)[└├]── (.+)"

    def _generate_comment_content(self):
        """
        helper method used in
        ``.generate_preview_tree()`` and ``.generate_prompt()``


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

    def __contains__(self, key):
        """
        allow ``PromptBlueprint`` to perform membership tests with key being


        :param key: hash of node; or node object
        :type key: int or PromptCorpusNode
        :return: if blueprint contains the node
        :rtype: bool
        """
        if isinstance(key, PromptCorpusNode):
            key = hash(key)

        return super().__contains__(key)

    def __repr__(self):
        """
        :return:
        :rtype: str
        :example:
        assert repr(node) == "PromptBlueprint(My Blueprint)"
        """
        return "PromptBlueprint({})".format(self.display_name)

    def __str__(self):
        """
        :return: equivalent to self.generate_preview_tree()
        :rtype: str
        """
        # BUG need test
        return self.generate_preview_tree()


# helpers  #####################################################################


def _add_all_unprunable_nodes_recursively(old_bp, pruned_bp, node):
    """
    recursively walk ``node``, and add necessary nodes from ``old_bp`` to
    ``pruned_bp``, such that trivial branches are pruned in the ``pruned_bp``

    (helper method used in ``PromptBlueprint.prune()``)


    :param old_bp:
    :type old_bp: PromptBlueprint
    :param pruned_bp:
    :type pruned_bp: PromptBlueprint
    :param node:
    :type node: PromptCorpusNode
    :return: if ``node`` has any checkmarked descents
    :rtype: bool
    """
    node_hash = hash(node)
    # if current node is checkmarked
    is_checkmarked = old_bp[node_hash]

    # if any of dependents is checkmarked
    has_checkmarked_descents = not node.is_leaf and any(
        _add_all_unprunable_nodes_recursively(old_bp, pruned_bp, child)
        for child in node.children
    )

    if is_checkmarked or has_checkmarked_descents:
        # this node should be in the pruned_bp
        pruned_bp[node_hash] = is_checkmarked
        return True
    else:
        return False


def _create_pruned_tree_for_preview_recursively(blueprint, node):
    """
    create a `PromptCorpusNode` as root of a new **pruned** tree such that
    only nodes contained in `blueprint` is kept.
    This is done by traverse the tree and check if any nodes is contained
    in the blueprint

    (helper method used in ``PromptBlueprint.generate_preview_tree()``)


    :param blueprint:
    :type blueprint: PromptBlueprint
    :param node:
    :type node: PromptCorpusNode
    :return: root of the filtered node
    :rtype: PromptCorpusNode
    """
    new_node = copy(node)  # an copy w/o children

    for child in node.children:
        if hash(child) in blueprint:
            new_child = _create_pruned_tree_for_preview_recursively(
                blueprint, child
            )
            new_child.parent = new_node

    return new_node


class PromptBlueprintOld:  # HACK rm

    def generate_prompt(self, *, hide_comment=False):
        # generate lines from root node
        lines = self._generate_prompt_recursively(self.prompt_corpus)

        # create comment part
        if not hide_comment:
            comment_line = (
                "<!-- " + self._generate_preview_tree_comment_line() + " -->"
            )
            lines.append(comment_line)

        return "\n".join(lines)

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
