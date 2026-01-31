"""
define `PromptBlueprint`
"""

import re
from datetime import datetime
from copy import copy

import importlib.metadata
from anytree import RenderTree, PreOrderIter

from .prompt_corpus_node import PromptCorpusNode

# TODO allows "merging" 2 blueprints

__all__ = ("PromptBlueprint",)


# constants  ###################################################################
CHECKMARKED_PREFIX = "[x] "
UNCHECKMARKED_PREFIX = "[ ] "
EMPTY_PREFIX = "    "


class PromptBlueprint(dict):
    """
    `PromptCorpusNode` represents a configurable subset of *prompt corpus tree*


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
        :raise ValueError: bad formatted `blueprint_text`
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
                    raise ValueError(
                        "malformed tree format at line:\n{}".format(line)
                    )

                path = previous_path + [""]

            elif level == previous_level:
                path = previous_path

            else:
                path = previous_path[: level + 1]

            path[level] = heading
            path_tuple = tuple(path)

            # check node's existence in tree  ----------------------------------
            if path_tuple not in path2node_hash:
                raise ValueError(
                    "missing node from prompt_corpus:\n{}".format(line)
                )

            # append a node  ---------------------------------------------------
            node_hash = path2node_hash[path_tuple]
            bp[node_hash] = is_checkmarked

            # update loop vars  ------------------------------------------------
            previous_level, previous_path = level, path

        # prune the tree
        return bp if disable_prune else bp.prune()

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
        return cls._create_full_or_empty_blueprint(
            prompt_corpus, True, display_name
        )

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
        return cls._create_full_or_empty_blueprint(
            prompt_corpus, False, display_name
        )

    def __init__(self, prompt_corpus, *, display_name=""):
        super().__init__()  # init as empty dict
        self.corpus = prompt_corpus
        self.display_name = display_name

    def is_checkmarked(self, node):
        """
        :param node: node object; or hash value of node
        :type node: PromptCorpusNode or int
        :raises TypeError:
        :return: whether a node is **checkmarked** in the blueprint;
                also ``False`` if node is not contained in blueprint
        :rtype: bool
        """
        node = _normalize_node_hash(node)  # node as hash
        return node in self and self[node]

    def prune(self):
        """
        :return: a **pruned** blueprint (of ``self``)
                which contains only branches with checkmarked nodes
        :rtype: PromptBlueprint
        """
        pruned_bp = PromptBlueprint(
            self.corpus, display_name=self.display_name
        )
        _add_all_unprunable_nodes_recursively(self, pruned_bp, self.corpus)
        return pruned_bp

    def checkmark(self, node):
        """
        checkmark a ``node`` in this blueprint


        :param node: node object; or hash value of node
        :type node: PromptBlueprint or int
        :raise TypeError:
        :raise ValueError:
        :return: self
        :rtype: PromptBlueprint
        """
        node_hash = _normalize_node_hash(node)

        if not _checkmark_find_node_recursively(node, self.corpus):
            raise ValueError(
                "node missing from blueprint's corpus: {}".format(repr(node))
            )

        self[node_hash] = True

        return self

    def uncheckmark(self, node):
        """
        uncheckmark a ``node`` in this blueprint


        :param node: node object; or hash value of node
        :type node: PromptBlueprint or int
        :raise TypeError:
        :raise KeyError:
        :return: self
        :rtype: PromptBlueprint
        """
        node_hash = _normalize_node_hash(node)

        if node_hash not in self:
            raise KeyError(
                "fail to uncheckmark node, missing in this blueprint: {}"
                .format(repr(node))
            )

        self[node_hash] = False

        return self

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
                CHECKMARKED_PREFIX
                if self.is_checkmarked(node)
                else UNCHECKMARKED_PREFIX
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
        render the **concrete prompt** that can be used as LLM system message
        with it content based on node's checkmarking status of this blueprint


        :param hide_comment: disable comment part after last line;
                defaults to False
        :type hide_comment: bool, optional
        :return: the generated prompt
        :rtype: str
        """
        lines = _generate_prompt_recursively(self, self.corpus)

        # create comment line
        if not hide_comment:
            comment_line = "<!-- " + self._generate_comment_content() + " -->"
            lines.append(comment_line)

        return "\n".join(lines).strip("\n")

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

    HEADING_LINE_PATTERN = r"\[([x ])\] (.*)[└├]── (.+)"

    @classmethod
    def _create_full_or_empty_blueprint(
        cls, prompt_corpus, is_full, display_name
    ):
        """
        helper method used
        in ``._create_full_blueprint()`` & in ``_create_empty_blueprint()``,
        i.e. a generic version of the 2 functions
        """
        blueprint = PromptBlueprint(prompt_corpus, display_name=display_name)
        # include all nodes
        for node in PreOrderIter(prompt_corpus):
            if not node.is_root:  # skip root node
                key = hash(node)
                # add all nodes
                blueprint[key] = is_full

        return blueprint

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

    def copy(self):
        copied = PromptBlueprint(self.corpus, display_name=self.display_name)

        # todo PromptBlueprint copy routine optimize
        for k, v in self.items():
            copied[k] = v

        return copied

    def __contains__(self, key):
        """
        allow ``PromptBlueprint`` to perform membership tests with key being


        :param key: node object; or hash value of node
        :type key: PromptCorpusNode or int
        :raises TypeError:
        :return: if blueprint contains the node
        :rtype: bool
        """
        return super().__contains__(_normalize_node_hash(key))

    def __iadd__(self, other):
        """
        checkmark a ``node`` in this blueprint

        (wrapper of and identical to ``.checkmark()``)


        :param node: node object; or hash value of node
        :type node: PromptBlueprint or int
        :raise TypeError:
        :raise ValueError:
        :return: self
        :rtype: PromptBlueprint
        """
        return self.checkmark(other)

    def __isub__(self, other):
        """
        uncheckmark a ``node`` in this blueprint

        (wrapper of and identical to ``.uncheckmark()``)


        :param node: node object; or hash value of node
        :type node: PromptBlueprint or int
        :raise TypeError:
        :raise KeyError:
        :return: self
        :rtype: PromptBlueprint
        """
        return self.uncheckmark(other)

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
        return self.merge(other)

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


def _generate_prompt_recursively(blueprint, node):
    """
    recursively traverse tree and only select nodes that is checkmarked in
    blueprint. Create the prompt by combining these nodes' content.

    (helper method used in ``PromptBlueprint.generate_prompt()``)


    :param blueprint:
    :type blueprint: PromptBlueprint
    :param node:
    :type node: PromptCorpusNode
    :return: prompt lines
    :rtype: list[str]
    """
    lines = []

    # add current node if checkmarked
    if blueprint.is_checkmarked(node):
        # pylint: disable-next=protected-access
        lines.extend(node._generate_prompt_lines())

    # add descendent
    for child in node.children:
        lines.extend(_generate_prompt_recursively(blueprint, child))

    return lines


def _normalize_node_hash(node):
    """
    :param node: node object; or hash value of node
    :type node: PromptCorpusNode or int
    :raises TypeError:
    :return: hash of node
    :rtype: int
    """
    if isinstance(node, PromptCorpusNode):
        return hash(node)

    elif isinstance(node, int):  # already hash
        return node

    else:
        raise TypeError(
            "must be PromptCorpusNode or hash value, not: {}".format(
                repr(node)
            )
        )


def _checkmark_find_node_recursively(target, node):
    """
    recursively traverse node and find if target is present in the tree

    (helper method used in ``PromptBlueprint.checkmark()``)


    :param target: node object; or hash value of node
    :type target: PromptCorpusNode or int
    :param node:
    :type node: PromptCorpusNode
    :return: whether `target` existed in tree of `node`
    :rtype: bool
    """
    if node is target or (isinstance(target, int) and hash(node) == target):
        # find the target node
        return True
    elif node.is_leaf:
        # reach bottom of tree
        return False

    return any(
        _checkmark_find_node_recursively(target, child)
        for child in node.children
    )
