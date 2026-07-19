"""
prompt_blueprint.py

define `PromptBlueprint`
"""

import copy

from anytree import PreOrderIter

from kaye.prompt.sidecar_nodes import (
    BlueprintDescriptorSidecars,
    get_sidecar_node_type,
)

from ..base_prompt_node import BasePromptNode
from ..prompt_corpus_loader import load_prompt_corpus_tree

from . import render
from . import parser
from .node_resolver import resolve_node

__all__ = ("PromptBlueprint",)


class PromptBlueprint(dict):
    """
    `PromptBlueprint` represents a configurable subset of *prompt corpus tree*


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
        disable_prune=False,
        corpus_override=None,
    ):
        """
        parse ``blueprint_text`` into a blueprint object


        :param blueprint_text: prompt blueprint text to set nodes, must in
                the same format of output of ``.generate_blueprint()``
                (with tree structure and checkmarks)
        :type blueprint_text: str
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
        bp = PromptBlueprint(corpus_override=corpus_override)

        bp.update(
            parser.parse_blueprint_text(blueprint_text, bp.corpus)
        )

        # prune the tree
        return bp if disable_prune else bp.prune()

    @classmethod
    def create_full_blueprint(cls, *, corpus_override=None):
        """
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
            True, corpus_override
        )

    @classmethod
    def create_empty_blueprint(cls, *, corpus_override=None):
        """
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
            False, corpus_override
        )

    @classmethod
    def create_from_node(cls, node, *, recursively=False):
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
        bp = cls.create_empty_blueprint()
        node_obj, _ = resolve_node(bp.corpus, node)
        bp.checkmark(node_obj, recursively=recursively)

        bp.sidecars = BlueprintDescriptorSidecars(main_node=node_obj)

        return bp

    # instance methods  ========================================================
    def __init__(self, *, corpus_override=None):
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

        self.sidecars = BlueprintDescriptorSidecars()

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
        _, node_hash = resolve_node(self.corpus, node)
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

    def generate_blueprint(self, **kwargs):
        """
        generate **preview tree** of the blueprint,
        an human-readable representation

        (see ``render.render_blueprint_tree()`` for parameters)


        :return: the preview tree
        :rtype: str
        """
        return render.render_blueprint_tree(self, **kwargs)

    def generate_prompt(self, **kwargs):
        """
        render the **concrete prompt** that can be used as LLM system message
        from this blueprint's node checkmarking status

        (see ``render.render_prompt_lines()`` for parameters)


        :return: generated prompt
        :rtype: str
        """
        return "\n".join(render.render_prompt_lines(self, **kwargs))

    # Blueprint operation  *****************************************************

    def prune(self):
        """
        :return: a **pruned** blueprint (of ``self``)
                which is a minimum version
                that contains only branches with checkmarked nodes
        :rtype: PromptBlueprint
        """
        # create bp w/ nothing
        pruned_bp = PromptBlueprint(corpus_override=self.corpus)

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

        merged = PromptBlueprint(corpus_override=self.corpus)

        merged.sidecars = self.sidecars | other.sidecars

        for k in keys:
            merged[k] = self.is_checkmarked(k) or other.is_checkmarked(k)

        return merged

    # helpers  =================================================================

    @classmethod
    def _create_full_or_empty_blueprint_generic(
        cls, is_full, corpus_override=None
    ):
        """
        helper method used
        in ``.create_full_blueprint()`` & in ``.create_empty_blueprint()``,
        i.e. a generic version of the 2 functions
        """
        bp = PromptBlueprint(corpus_override=corpus_override)

        # include all nodes; sidecar nodes are never auto-checkmarked
        for node in PreOrderIter(bp.corpus):
            if not node.is_root:  # skip root node
                key = hash(node)
                bp[key] = is_full and not bool(get_sidecar_node_type(node))

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
        node_obj, node_hash = resolve_node(self.corpus, node)

        if node_hash not in self and not is_checkmark:
            raise ValueError(
                "node not contained in blueprint: {}".format(node_obj)
            )

        # actual perform checking/unchecking
        self[node_hash] = is_checkmark

        # add all descendants too; skip sidecar nodes when auto-checkmarking
        if recursively:
            for d in node_obj.descendants:
                if is_checkmark and bool(get_sidecar_node_type(d)):
                    continue
                d_hash = hash(d)
                if d_hash in self or is_checkmark:
                    self[d_hash] = is_checkmark

        return self

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
            _, node_hash = resolve_node(self.corpus, key)
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
        copied = PromptBlueprint(corpus_override=self.corpus)

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


# helpers  #####################################################################


def _add_all_unprunable_nodes_recursively(old_bp, pruned_bp, node):
    """
    recursively walk ``node``, and add necessary nodes from ``old_bp`` to
    ``pruned_bp``, such that trivial branches are pruned in the ``pruned_bp``

    (helper function used in ``PromptBlueprint.prune()``)


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

    # traverse all children
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
