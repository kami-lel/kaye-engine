"""
index.py

define ``NodePath``, ``CorpusIndex``, and ``get_corpus_index`` -- arrays
and masks derived once from the process's one corpus tree
"""

from dataclasses import dataclass

from anytree import PreOrderIter

from ..base_prompt_node import BasePromptNode
from ..prompt_corpus_loader import add_corpus_clear_hook, get_corpus_tree

__all__ = (
    "CorpusIndex",
    "NodePath",
    "get_corpus_index",
)

# lineage below root, root is ()
NodePath = tuple[str, ...]

# the lazily built index of the loaded corpus tree
_corpus_index = None


@dataclass(frozen=True, slots=True, eq=False)
class CorpusIndex:  ############################################################
    """
    structural arrays of the corpus tree, one entry per node, indexed by
    the node's pre-order position -- that position is also the node's bit
    in every mask


    :param node_objs: the nodes, in pre-order
    :type node_objs: tuple[BasePromptNode, ...]
    :param paths: each node's lineage below root
    :type paths: tuple[NodePath, ...]
    :param depths: each node's depth, 0 at root
    :type depths: tuple[int, ...]
    :param parent_idxs: each node's parent position, -1 at root
    :type parent_idxs: tuple[int, ...]
    :param child_idxs: each node's children positions, in sibling order
    :type child_idxs: tuple[tuple[int, ...], ...]
    :param subtree_masks: each node's bit OR-ed with every descendant's
    :type subtree_masks: tuple[int, ...]
    :param idx_by_path: node position by path
    :type idx_by_path: dict[NodePath, int]
    """

    node_objs: tuple[BasePromptNode, ...]
    paths: tuple[NodePath, ...]
    depths: tuple[int, ...]
    parent_idxs: tuple[int, ...]
    child_idxs: tuple[tuple[int, ...], ...]
    subtree_masks: tuple[int, ...]
    idx_by_path: dict[NodePath, int]


# auxiliaries  #################################################################
def _build_corpus_index(root):
    """
    :param root: root of the corpus tree
    :type root: BasePromptNode
    :return: the structural index of ``root``'s tree
    :rtype: CorpusIndex
    """
    node_objs = tuple(PreOrderIter(root))
    idx_of_node = {id(node): idx for idx, node in enumerate(node_objs)}

    paths = tuple(tuple(node.generate_lineage()) for node in node_objs)
    depths = tuple(node.depth for node in node_objs)
    parent_idxs = tuple(
        -1 if node.is_root else idx_of_node[id(node.parent)]
        for node in node_objs
    )
    child_idxs = tuple(
        tuple(idx_of_node[id(child)] for child in node.children)
        for node in node_objs
    )

    # descendants sit after their ancestor in pre-order, so a reverse
    # sweep sees every child's mask before its parent's
    subtree_masks = [0] * len(node_objs)
    for idx in range(len(node_objs) - 1, -1, -1):
        mask = 1 << idx
        for child_idx in child_idxs[idx]:
            mask |= subtree_masks[child_idx]
        subtree_masks[idx] = mask

    return CorpusIndex(
        node_objs=node_objs,
        paths=paths,
        depths=depths,
        parent_idxs=parent_idxs,
        child_idxs=child_idxs,
        subtree_masks=tuple(subtree_masks),
        idx_by_path={path: idx for idx, path in enumerate(paths)},
    )


def _drop_corpus_index():
    global _corpus_index  # pylint: disable=global-statement

    _corpus_index = None


add_corpus_clear_hook(_drop_corpus_index)


# Public API  ##################################################################
def get_corpus_index():
    """
    Prerequisite: :func:`load_corpus_tree` called


    :raises ValueError: no corpus tree is loaded yet
    :return: the index of the loaded corpus tree, built on first use and
            dropped by :func:`clear_corpus_tree`
    :rtype: CorpusIndex
    """
    global _corpus_index  # pylint: disable=global-statement

    if _corpus_index is None:
        _corpus_index = _build_corpus_index(get_corpus_tree())

    return _corpus_index
