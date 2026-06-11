"""
prompt_blueprint.py

define `PromptBlueprint`
"""

import re
from datetime import datetime
import copy

import importlib.metadata
from anytree import RenderTree, PreOrderIter


from .base_prompt_node import BasePromptNode
from .prompt_corpus_loader import (
    load_prompt_corpus_tree,
    HEADING_PREFIX_ELEMENT,
)

__all__ = ("PromptBlueprint",)


# Fixme better description handling: use {description} & not rendered in prompt;
# FIXME split style guide

# constants  ###################################################################
CHECKMARKED_PREFIX = "[x] "
UNCHECKMARKED_PREFIX = "[ ] "
EMPTY_PREFIX = "    "


class PromptBlueprint(dict):
    """
    `PromptBlueprint` represents a configurable subset of *prompt corpus tree*


    :param display_name: display name given to the blueprint
    :type display_name: str, optional
    :param corpus_override: use to set ``.corpus``,
            instead of using ``load_prompt_corpus_tree`` by default;
            defaults to None
    :type corpus_override: PromptCorpusNode, optional
    """

    # classmethods  ============================================================
    @classmethod
    def parse(
        cls,
        blueprint_text,
        *,
        display_name="",
        disable_prune=False,
        corpus_override=None,
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
        :param corpus_override: use to set ``.corpus``,
                instead of using ``load_prompt_corpus_tree`` by default;
                defaults to None
        :type corpus_override: PromptCorpusNode, optional
        :raise ValueError:
        :return: a blueprint parsed from ``blueprint_text``
        :rtype: PromptBlueprint
        """
        # create bp w/ nothing, to be filled during this function
        bp = PromptBlueprint(
            display_name=display_name,
            corpus_override=corpus_override,
        )

        # extract all headings  ++++++++++++++++++++++++++++++++++++++++++++++++
        prev_node = bp.corpus
        for line in blueprint_text.split("\n"):
            heading_line_match = cls.HEADING_LINE_PATTERN.fullmatch(line)

            if not heading_line_match:
                continue  # skip line that is not a node heading

            # extract info for current node
            is_checkmarked = heading_line_match.group(1) == "x"
            level = len(heading_line_match.group(2)) // 4 + 1
            heading = heading_line_match.group(3)

            # find parent of current node
            level_offset = level - prev_node.depth
            if level_offset > 1:
                raise ValueError(
                    "malformed tree format at line:\n{}".format(line)
                )

            elif level_offset > 0:
                parent = prev_node

            else:
                parent = prev_node.ancestors[level - 1]

            # create/add node
            node = bp._parse_add_corpus_node(parent, heading, line)

            # include node in the blueprint
            bp[hash(node)] = is_checkmarked

            prev_node = node

        # prune the tree
        return bp if disable_prune else bp.prune()

    @classmethod
    def create_full_blueprint(
        cls, *, display_name="full", corpus_override=None
    ):
        """
        :param display_name:
        :type display_name: str, optional
        :param corpus_override: use to set ``.corpus``,
                instead of using ``load_prompt_corpus_tree`` by default;
                defaults to None
        :type corpus_override: PromptCorpusNode, optional
        :return: a blueprint
                with all nodes from `prompt_corpus` (except dynamic nodes,)
                and checkmarking all nodes
        :rtype: PromptBlueprint
        """
        return cls._create_full_or_empty_blueprint_generic(
            True, display_name, corpus_override
        )

    @classmethod
    def create_empty_blueprint(
        cls, *, display_name="empty", corpus_override=None
    ):
        """
        :param display_name:
        :type display_name: str, optional
        :param corpus_override: use to set ``.corpus``,
                instead of using ``load_prompt_corpus_tree`` by default;
                defaults to None
        :type corpus_override: PromptCorpusNode, optional
        :return: a blueprint
                with all nodes from `prompt_corpus` (except dynamic nodes,)
                but uncheckmarking all nodes
        :rtype: PromptBlueprint
        """
        return cls._create_full_or_empty_blueprint_generic(
            False, display_name, corpus_override
        )

    @classmethod
    def create_from_node(self, node, *, recursively=False):
        """
        create a **blueprint** from a specific node and its content

        generates a blueprint containing only the specified node
        (and optionally all its descendants). automatically extracts
        the node's description subnode content (if present) and includes
        it as the blueprint's description, enabling LLM task relevance
        assessment. useful for creating focused prompts from individual
        corpus sections.


        :param node: node object; hash value; name
        :type node: BasePromptNode or int or str
        :param recursively: allow checkmarks on node's descendants,
                defaults to False
        :type recursively: bool, optional
        :raise TypeError:
        :raise ValueError:
        """
        bp = PromptBlueprint.create_empty_blueprint()
        node_obj, _ = bp._find_node_in_corpus_and_blueprint(node)
        bp.checkmark(node_obj, recursively=recursively)

        bp.display_name = node_obj.name

        description_node = node_obj.description_subnode
        if description_node:
            description_bp = PromptBlueprint.create_from_node(description_node)
            bp.description = description_bp.generate_prompt(
                disable_first_heading=True
            )

        return bp

    # instance methods  ========================================================
    def __init__(self, *, display_name="", corpus_override=None):
        super().__init__()  # init as empty dict

        if corpus_override is None:
            self.corpus = load_prompt_corpus_tree()
        else:
            if not (
                isinstance(corpus_override, BasePromptNode)
                and (corpus_override.is_root)
            ):
                raise ValueError(
                    "kwarg corpus_override must be a root node: {}".format(
                        corpus_override
                    )
                )
            self.corpus = copy.deepcopy(corpus_override)

        self.display_name = display_name
        self.description = ""

    # node operations  *********************************************************
    def is_checkmarked(self, node):
        """
        :param key: node object; hash value; name
        :type node: BasePromptNode or int or str
        :raises TypeError:
        :raise ValueError:
        :return: whether a node is **checkmarked** in the blueprint;
                ``False`` if node is: not checkmarked or not contained
        :rtype: bool
        """
        _, node_hash = self._find_node_in_corpus_and_blueprint(node)
        return node_hash in self and self[node_hash]

    def checkmark(self, node, *, recursively=False):
        """
        checkmark a ``node`` in this blueprint
        (will add node into this blueprint if not, then checkmarked it)


        :param node: node object; hash value; name
        :type node: BasePromptNode or int or str
        :param recursively: allow checkmarks on node's descendants,
                defaults to False
        :type recursively: bool, optional
        :raise TypeError:
        :raise ValueError:
        :return: self
        :rtype: PromptBlueprint
        """
        return self._checkmark_or_uncheckmark_generic(node, recursively, True)

    def uncheckmark(self, node, *, recursively=False):
        """
        uncheckmark a ``node`` in this blueprint
        (node must be contained in this blueprint)


        :param key: node object; hash value; name
        :type node: BasePromptNode or int or str
        :param recursively: allow checkmarks on node's descendants,
                defaults to False
        :type recursively: bool, optional
        :raise TypeError:
        :raise ValueError:
        :raise KeyError: given ``node`` is not contained in this blueprint
        :return: self
        :rtype: PromptBlueprint
        """
        return self._checkmark_or_uncheckmark_generic(node, recursively, False)

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
                if self.is_checkmarked(hash(node))
                else UNCHECKMARKED_PREFIX
            )
            if node.is_root:
                checkmark_prefix = EMPTY_PREFIX

            # e.g. "[x] │   └── Capitalization Style"
            node_line = checkmark_prefix + pre + node.name
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

    def generate_prompt(
        self, *, show_comment=False, disable_first_heading=False, **kwargs
    ):
        """
        render the **concrete prompt** that can be used as LLM system message
        with it content based on node's checkmarking status of this blueprint


        :param show_comment: show comment part after last line;
                defaults to False
        :type show_comment: bool, optional
        :param disable_first_heading: whether disable showing top heading;
                defaults to False
        :type disable_first_heading: bool, optional
        :return: generated prompt
        :rtype: str
        """
        # todo compact render & other types
        lines = []

        should_skip_heading = disable_first_heading

        last_node_idx = self.corpus.size - 1
        for i, node in enumerate(PreOrderIter(self.corpus)):
            if self.is_checkmarked(node):
                if should_skip_heading:
                    should_skip_heading = False
                else:
                    # heading line
                    lines.append(
                        HEADING_PREFIX_ELEMENT * node.depth + " " + node.name
                    )

                # content lines
                content_lines = node.content_lines(**kwargs)
                if content_lines:
                    lines.extend(content_lines)
                    if i != last_node_idx:
                        lines.append("")  # add an empty line

        if show_comment:
            lines.append("<!-- " + self._generate_comment_content() + " -->")

        # trim empty lines
        while lines and lines[0] == "":
            lines.pop(0)

        while lines and lines[-1] == "":
            lines.pop()

        return "\n".join(lines)

    # Blueprint operation  *****************************************************

    def prune(self):
        """
        :return: a **pruned** blueprint (of ``self``)
                which is a minimum version
                that contains only branches with checkmarked nodes
        :rtype: PromptBlueprint
        """
        # create bp w/ nothing
        pruned_bp = PromptBlueprint(
            display_name=self.display_name, corpus_override=self.corpus
        )

        _add_all_unprunable_nodes_recursively(self, pruned_bp, self.corpus)

        return pruned_bp

    def merge(self, other):
        """
        create a new **merged** blueprint as union of checkmarked nodes


        :param other:
        :type other: PromptBlueprint
        :raises ValueError:
        :return: merged blueprint
        :rtype: PromptBlueprint
        """
        if self.corpus != other.corpus:
            raise ValueError("must merge blueprint of same prompt tree")

        # create keys of resulted blueprint
        keys = set(self.keys()) | set(other.keys())

        # create display_name
        display_name = "|".join(
            name for name in (self.display_name, other.display_name) if name
        )

        merged = PromptBlueprint(
            display_name=display_name, corpus_override=self.corpus
        )

        for k in keys:
            merged[k] = self.is_checkmarked(k) or other.is_checkmarked(k)

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

    def _parse_add_corpus_node(self, parent, heading, line):
        """
        find current node when non-dynamic, and include it in this blueprint

        (helper method used in ``.parse()``)
        """
        try:
            return parent[heading]
        except KeyError as err:
            raise ValueError(
                "missing node heading {} in corpus "
                "that corresponds to this line:\n{}".format(repr(heading), line)
            ) from err

    @classmethod
    def _create_full_or_empty_blueprint_generic(
        cls, is_full, display_name, corpus_override=None
    ):
        """
        helper method used
        in ``.create_full_blueprint()`` & in ``.create_empty_blueprint()``,
        i.e. a generic version of the 2 functions
        """
        bp = PromptBlueprint(
            display_name=display_name,
            corpus_override=corpus_override,
        )

        # include all nodes
        for node in PreOrderIter(bp.corpus):
            if not node.is_root:  # skip root node
                key = hash(node)
                # add all nodes
                bp[key] = is_full

        return bp

    def _checkmark_or_uncheckmark_generic(
        self, node, recursively, is_checkmark
    ):
        """
        helper method used
        in ``.checkmark()`` & in ``.uncheckmark()``,
        i.e. a generic version of the 2 functions


        :raises TypeError:
        :raises ValueError:
        """
        # find node in corpus
        node_obj, node_hash = self._find_node_in_corpus_and_blueprint(node)

        if node_hash not in self and not is_checkmark:
            raise ValueError(
                "node not contained in blueprint: {}".format(node_obj)
            )

        # actual perform checking/unchecking
        self[node_hash] = is_checkmark

        # add all descendants too
        if recursively:
            for d in node_obj.descendants:
                d_hash = hash(d)
                if d_hash in self or is_checkmark:
                    self[d_hash] = is_checkmark

        return self

    def _find_node_in_corpus_and_blueprint(self, node_arg):
        """
        helper method used in:

        - ``.checkmark()``
        - ``.uncheckmark()``
        - ``.is_checkmarked()``
        - ``.__contains__()``

        to search a node in corpus providing node object/name/hash


        :raises TypeError:
        :raises ValueError:
        """
        corpus_and_descendants = [self.corpus] + list(self.corpus.descendants)

        # search by name   -----------------------------------------------------
        if isinstance(node_arg, str):
            node_obj = None

            # search all descendants with name of node
            for n in corpus_and_descendants:
                if node_arg == n.name:
                    node_obj = n
                    break

            if node_obj is None:
                raise ValueError(
                    "no node in corpus with name: {}".format(repr(node_arg))
                )

            node_hash = hash(node_obj)

        # search by node hash  -------------------------------------------------
        elif isinstance(node_arg, int):
            node_obj = None

            # search all descendants with hash of node
            for n in corpus_and_descendants:
                if node_arg == hash(n):
                    node_obj = n
                    break

            if node_obj is None:
                raise ValueError(
                    "no node in corpus with hash value: {}".format(
                        repr(node_arg)
                    )
                )

            node_hash = node_arg

        # node is already object  ----------------------------------------------
        elif isinstance(node_arg, BasePromptNode):
            if node_arg not in corpus_and_descendants:
                raise ValueError("node not in corpus: {}".format(node_arg))

            node_obj = node_arg
            node_hash = hash(node_arg)

        else:
            raise TypeError(
                "must be BasePromptNode/int(hash value)/str(name): {}".format(
                    node_arg
                )
            )

        return node_obj, node_hash

    # magic methods  ===========================================================

    def __contains__(self, key):
        """
        allow ``PromptBlueprint`` to perform membership tests


        :param key: node object; hash value; name
        :type key: PromptCorpusNode or int or str
        :raises ValueError:
        :return: if blueprint contains the node
        :rtype: bool
        """
        if isinstance(key, int):
            return super().__contains__(key)

        try:
            _, node_hash = self._find_node_in_corpus_and_blueprint(key)
            return super().__contains__(node_hash)

        except TypeError:
            return NotImplemented

    # operators  ---------------------------------------------------------------

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
        if isinstance(other, (BasePromptNode, int, str)):
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
        if isinstance(other, (BasePromptNode, int, str)):
            return self.uncheckmark(other)
        else:
            return NotImplemented

    def __or__(self, other):
        """
        create a merged blueprint

        (wrapper of and identical to ``.merge()``)


        :param other:
        :type other: PromptBlueprint
        :raises ValueError:
        :return: merged blueprint
        :rtype: PromptBlueprint
        """
        if not isinstance(other, PromptBlueprint):
            return NotImplemented

        return self.merge(other)

    # copy  --------------------------------------------------------------------

    def __copy__(self):
        """
        :return: shallow copy, w/o creating new node tree
        :rtype: PromptBlueprint
        """
        copied = PromptBlueprint(
            display_name=self.display_name, corpus_override=self.corpus
        )

        for k, v in self.items():
            copied[k] = v

        return copied

    def __deepcopy__(self, memo):
        """
        :param memo:
        :type memo:
        :return: deep copy, and creating new tree of copied nodes
        :rtype: PromptBlueprint
        """
        copied = copy.copy(self)

        # create a new tree
        copied.corpus = copy.deepcopy(self.corpus)

        return copied

    # str  ---------------------------------------------------------------------

    def __repr__(self):
        """
        :return: equivalent to ``self.generate_blueprint()``
        :rtype: str
        """
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
