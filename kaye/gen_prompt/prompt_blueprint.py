"""
define `PromptBlueprint`
"""

import re
from datetime import datetime
import copy
from enum import Enum, auto

import importlib.metadata
from anytree import RenderTree, PreOrderIter


from .base_prompt_node import BasePromptNode
from .prompt_corpus_loader import get_prompt_corpus_tree, HEADING_PREFIX_ELEMENT

# from .prompt_corpus_loader import load_embedded_prompt_corpus
from .today_node import TodayNode

__all__ = ("PromptBlueprint",)


# constants  ###################################################################
CHECKMARKED_PREFIX = "[x] "
UNCHECKMARKED_PREFIX = "[ ] "
EMPTY_PREFIX = "    "


class PromptBlueprint(dict):
    """
    `PromptBlueprint` represents a configurable subset of *prompt corpus tree*


    :param display_name: display name given to the blueprint
    :type display_name: str, optional
    :param prompt_corpus_override: (for testing only;) defaults to None
    :type prompt_corpus_override: PromptCorpusNode, optional
    """

    # classmethods  ============================================================
    @classmethod
    def parse(
        cls,
        blueprint_text,
        *,
        display_name="",
        disable_prune=False,
        prompt_corpus_override=None,
    ):
        """
        parse ``blueprint_text`` into a blueprint object


        :param blueprint_text: prompt blueprint text to set nodes, must in
                the same format of output of ``.generate_blueprint()``
                (with tree structure and checkmarks)
        :type blueprint_text: str
        :param display_name: defaults to ""
        :type display_name: str, optional
        :type display_name: str, optional
        :param disable_prune: by default,
                the parsed tree does not include irreverent nodes;
                when ``disable_prune``, the parsed tree contains the full
                prompt corpus tree
        :type disable_prune: bool, optional
        :param prompt_corpus_override: (for testing only), defaults to None
        :type prompt_corpus_override: PromptCorpusNode, optional
        :raise ValueError: bad formatted `blueprint_text`
        :return: a blueprint parsed from ``blueprint_text``
        :rtype: PromptBlueprint
        """
        # create bp w/ nothing, to be filled during this function
        bp = PromptBlueprint(
            display_name=display_name,
            prompt_corpus_override=prompt_corpus_override,
        )

        # mapping id lineage : hash(all node in corpus)
        id_lineage2node_hash = {
            tuple(node.generate_id_lineage()): hash(node)
            for node in bp.corpus.descendants
        }
        # extract all headings  ++++++++++++++++++++++++++++++++++++++++++++++++
        previous_level = -1
        previous_path = []
        for line in blueprint_text.split("\n"):
            heading_line_match = cls.HEADING_LINE_PATTERN.fullmatch(line)

            if not heading_line_match:
                continue  # skip line that is not a node heading

            is_checkmarked = heading_line_match.group(1) == "x"
            level = len(heading_line_match.group(2)) // 4
            heading = heading_line_match.group(3)

            # dynamically decide path  -----------------------------------------
            if level > previous_level:

                if level - previous_level > 1:
                    raise ValueError(
                        "malformed tree format at line:\n{}".format(line)
                    )

                path = previous_path + [""]

            elif level == previous_level:
                path = previous_path

            else:
                path = previous_path[: level + 1]

            path[level] = heading

            # attach node to blueprint  ----------------------------------------
            # TODO how to deal w/ dynamic blueprint

            path_tuple = tuple(path)

            # check node's existence in tree  ----------------------------------
            if path_tuple not in id_lineage2node_hash:
                raise ValueError(
                    "no node in prompt corpus tree that "
                    "corresponds to this line:\n{}".format(line)
                )

            # append a node  ---------------------------------------------------
            node_hash = id_lineage2node_hash[path_tuple]
            bp[node_hash] = is_checkmarked

            # update loop vars  ------------------------------------------------
            previous_level, previous_path = level, path

        # prune the tree
        return bp if disable_prune else bp.prune()

    @classmethod
    def create_full_blueprint(
        cls, *, display_name="full", prompt_corpus_override=None
    ):
        """
        :param display_name:
        :type display_name: str, optional
        :param prompt_corpus_override: (for testing only), defaults to None
        :type prompt_corpus_override: PromptCorpusNode, optional
        :return: a blueprint with all nodes from `prompt_corpus`,
                and checkmarking all nodes
        :rtype: PromptBlueprint
        """
        return cls._create_full_or_empty_blueprint(
            True, display_name, prompt_corpus_override
        )

    @classmethod
    def create_empty_blueprint(
        cls, *, display_name="empty", prompt_corpus_override=None
    ):
        """
        :param display_name:
        :type display_name: str, optional
        :param prompt_corpus_override: (for testing only), defaults to None
        :type prompt_corpus_override: PromptCorpusNode, optional
        :return: a blueprint with all nodes from `prompt_corpus`,
                but checkmarking all nodes
        :rtype: PromptBlueprint
        """
        return cls._create_full_or_empty_blueprint(
            False, display_name, prompt_corpus_override
        )

    # instance methods  ========================================================
    def __init__(self, *, display_name="", prompt_corpus_override=None):
        super().__init__()  # init as empty dict

        self.corpus = (
            get_prompt_corpus_tree()
            if prompt_corpus_override is None
            else prompt_corpus_override
        )

        self.display_name = display_name

    # node operations  *********************************************************
    def is_checkmarked(self, node_hash):
        """
        :param node: node object; or hash value of node
        :type node: BasePromptNode or int
        :raises TypeError:
        :return: whether a node is **checkmarked** in the blueprint;
                ``False`` if node is: not checkmarked or not contained
        :rtype: bool
        """
        node_hash = _normalize_as_node_hash(node_hash)  # node as hash
        return node_hash in self and self[node_hash]

    def checkmark(self, node):
        """
        checkmark a ``node`` in this blueprint


        :param node: node object; or hash value of node
        :type node: BasePromptNode or int
        :raise TypeError:
        :raise ValueError:
        :return: self
        :rtype: PromptBlueprint
        """
        node_hash = _normalize_as_node_hash(node)

        # assert node existed in corpus
        if not any(hash(node) == node_hash for node in self.corpus.descendants):
            raise ValueError(
                "node absent in prompt corpus tree: {}".format(str(node))
            )

        self[node_hash] = True

        return self

    def uncheckmark(self, node):
        """
        uncheckmark a ``node`` in this blueprint


        :param node: node object; or hash value of node
        :type node: BasePromptNode or int
        :raise TypeError:
        :raise KeyError:
        :return: self
        :rtype: PromptBlueprint
        """
        node_hash = _normalize_as_node_hash(node)

        if node_hash not in self:
            raise KeyError(
                "node absent in this blueprint: {}".format(str(node))
            )

        self[node_hash] = False

        return self

    def generate_blueprint(
        self,
        *,
        content_preview_lines=3,
        content_preview_width=64,
        show_full_tree=False,
        show_comment=False,
    ):
        """
        generate **preview tree** of the blueprint,
        an human-readable representation


        :param content_preview_lines: set maximum line count of
                *content preview* part, (excluding section heading line);
                defaults to 3
        :type content_preview_lines: int
        :param content_preview_width: set maximum column width of
                *content preview* part;
                defaults to 64.
        :type content_preview_width: int
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
        lines = []
        for pre, fill, node in RenderTree(preview_tree):
            # line for tree structure
            checkmark_prefix = (
                CHECKMARKED_PREFIX
                if self.is_checkmarked(node)
                else UNCHECKMARKED_PREFIX
            )
            if node.is_root:
                checkmark_prefix = EMPTY_PREFIX

            # e.g. "[x] │   └── Capitalization Style"
            node_line = checkmark_prefix + pre + node.id
            lines.append(node_line)

            # lines for content preview part
            if content_preview_lines:
                content_fill = EMPTY_PREFIX + fill
                lines.extend(
                    (content_fill + line)[:content_preview_width]
                    for line in node.content_lines()[:content_preview_lines]
                )

        # append comment line  -------------------------------------------------
        if show_comment:
            comment_line = "<!-- " + self._generate_comment_content() + " -->"
            lines.append(comment_line)

        return "\n".join(lines)

    # prompt creating  *********************************************************

    class Render(Enum):
        """
        specify rendering compactness for ``.generate_prompt()``


        e.g. for using ``NO_EMPTY_SPACE``::

            # Project Title
            ## First Heading
            Content of First Paragraph
            ## Second Heading
            ...

        e.g. for using ``COMPACT``::

            # Project Title
            ## First Heading
            Content of First Paragraph

            ## Second Heading
            Content of Second Paragraph

        e.g. for using ``LONG_FORMAT``::

            # Project Title

            ## First Heading

            Content of First Paragraph

            {additional 33 empty lines}
            ## Second Heading

            Content of Second Paragraph

        e.g. for using ``SHORT_FORMAT``::

            # Project Title

            ## First Heading

            Content of First Paragraph

            {additional 12 empty lines}
            ## Second Heading

            Content of Second Paragraph
        """

        NO_EMPTY_SPACE = auto()
        COMPACT = auto()
        LONG_FORMAT = auto()
        SHORT_FORMAT = auto()

    def generate_prompt(self, *, show_comment=False, render=Render.COMPACT):
        """
        render the **concrete prompt** that can be used as LLM system message
        with it content based on node's checkmarking status of this blueprint


        :param show_comment: show comment part after last line;
                defaults to False
        :type show_comment: bool, optional
        :return: generated prompt
        :rtype: str
        """
        # todo render type
        lines = []

        for node in PreOrderIter(self.corpus):
            if node in self:
                # heading line
                lines.append(
                    HEADING_PREFIX_ELEMENT * node.depth + " " + node.name
                )
                # content lines
                content_lines = node.content_lines()
                if content_lines:
                    lines.extend(content_lines)
                    lines.append("")  # add an empty line

        if show_comment:
            lines.append("<!-- " + self._generate_comment_content() + " -->")

        return "\n".join(lines)

    # Blueprint operation  *****************************************************

    def prune(self):
        """
        :return: a **pruned** blueprint (of ``self``)
                which contains only branches with checkmarked nodes
        :rtype: PromptBlueprint
        """
        # create bp w/ nothing
        pruned_bp = PromptBlueprint(
            display_name=self.display_name, prompt_corpus_override=self.corpus
        )

        _add_all_unprunable_nodes_recursively(self, pruned_bp, self.corpus)

        return pruned_bp

    def merge(self, other):
        """
        merging 2 blueprints, all nodes will be in the merged blueprint


        :param other:
        :type other: PromptBlueprint
        :raise TypeError:
        :raise ValueError:
        :return: merged blueprint
        :rtype: PromptBlueprint
        """
        # Bug
        if not isinstance(other, PromptBlueprint):
            raise TypeError(
                "must merge another PromptBlueprint, not: {}".format(
                    repr(other)
                )
            )

        if self.corpus is not other.corpus:
            raise ValueError("must merge 2 blueprints with same corpus")

        # perform merging
        merged = self.copy()  # based on self
        for k, right_v in other.items():
            left_v = k in merged and merged[k]
            merged_v = left_v or right_v
            merged[k] = merged_v

        return merged

    # helpers  =================================================================

    HEADING_LINE_PATTERN = re.compile(r"\[([x ])\] (.*)[└├]── (.+)")

    def _generate_comment_content(self):
        """
        (helper method used in
        ``.generate_blueprint()`` and ``.generate_prompt()``)


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

    @classmethod
    def _create_full_or_empty_blueprint(
        cls, is_full, display_name, prompt_corpus_override=None
    ):
        """
        helper method used
        in ``._create_full_blueprint()`` & in ``_create_empty_blueprint()``,
        i.e. a generic version of the 2 functions
        """
        bp = PromptBlueprint(
            display_name=display_name,
            prompt_corpus_override=prompt_corpus_override,
        )

        # include all nodes
        for node in PreOrderIter(bp.corpus):
            if not node.is_root:  # skip root node
                key = hash(node)
                # add all nodes
                bp[key] = is_full

        return bp

    # magic methods  ===========================================================

    def __contains__(self, key):
        """
        allow ``PromptBlueprint`` to perform membership tests with key being


        :param key: node object; or hash value of node
        :type key: PromptCorpusNode or int
        :raises TypeError:
        :return: if blueprint contains the node
        :rtype: bool
        """
        return super().__contains__(_normalize_as_node_hash(key))

    def __iadd__(self, other):
        """
        checkmark a ``node`` in this blueprint

        (wrapper of and identical to ``.checkmark()``)


        :param node: node object; or hash value of node
        :type node: BasePromptNode or int
        :raise TypeError:
        :raise ValueError:
        :return: self
        :rtype: PromptBlueprint
        """
        if isinstance(other, (BasePromptNode, int)):
            return self.checkmark(other)
        else:
            return NotImplemented

    def __isub__(self, other):
        """
        uncheckmark a ``node`` in this blueprint

        (wrapper of and identical to ``.uncheckmark()``)


        :param node: node object; or hash value of node
        :type node: BasePromptNode or int
        :raise TypeError:
        :raise KeyError:
        :return: self
        :rtype: PromptBlueprint
        """
        if isinstance(other, (BasePromptNode, int)):
            return self.uncheckmark(other)
        else:
            return NotImplemented

    def __imul__(self, other):
        """
        merging 2 blueprints

        (wrapper of and identical to ``.merge()``)


        :param other:
        :type other: PromptBlueprint
        :raise TypeError:
        :raise ValueError:
        :return: merged blueprint
        :rtype: PromptBlueprint
        """
        # Todo use return NotImplemented
        return self.merge(other)

    def __copy__(self):
        """
        :return: shallow copy, w/o creating new nodes
        :rtype: PromptBlueprint
        """
        copied = PromptBlueprint(
            display_name=self.display_name, prompt_corpus_override=self.corpus
        )

        for k, v in self.items():
            copied[k] = v

        return copied

    def __repr__(self):
        return self.generate_blueprint()

    def __str__(self):
        """
        :return:
        :rtype: str

        :example:
        >>> str(node)
        "PromptBlueprint(My Blueprint)"
        """
        return "PromptBlueprint({})".format(self.display_name)


# helpers  #####################################################################


def _normalize_as_node_hash(node):
    """
    :param node: node object; or hash value of node
    :type node: BasePromptNode or int
    :raises TypeError:
    :return: node hash value, regardless when provided node object or node hash
    :rtype: int
    """
    if isinstance(node, BasePromptNode):
        return hash(node)

    elif isinstance(node, int):  # already hash
        return node

    else:
        raise TypeError(
            "must be BasePromptNode or hash value: {}".format(repr(node))
        )


def _create_pruned_tree_for_preview_recursively(blueprint, node):
    """
    create a `PromptCorpusNode` as root of a new **pruned** tree such that
    only nodes contained in `blueprint` is kept.
    This is done by traverse the tree and check if any nodes is contained
    in the blueprint

    (helper method used in ``PromptBlueprint.generate_blueprint()``)


    :param blueprint:
    :type blueprint: PromptBlueprint
    :param node:
    :type node: BasePromptNode
    :return: root of the filtered node
    :rtype: PromptCorpusNode
    """
    new_node = copy.copy(node)  # an copy w/o children

    for child in node.children:
        if child in blueprint:
            new_child = _create_pruned_tree_for_preview_recursively(
                blueprint, child
            )
            new_child.parent = new_node

    return new_node


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
    is_checkmarked = old_bp.is_checkmarked(node)

    # traherne all children
    children_results = [
        _add_all_unprunable_nodes_recursively(old_bp, pruned_bp, child)
        for child in node.children
    ]

    # if any of dependents is checkmarked
    has_checkmarked_descents = any(children_results)

    if is_checkmarked or has_checkmarked_descents:
        if not node.is_root:
            # this node should be in the pruned_bp
            pruned_bp[node_hash] = is_checkmarked
        return True
    else:
        return False
