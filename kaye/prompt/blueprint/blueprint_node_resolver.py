"""
blueprint_node_resolver.py

define ``resolve_node``
"""

from ..base_prompt_node import BasePromptNode

__all__ = ("resolve_node",)


# auxiliaries  #################################################################
def _get_hash_index(corpus):
    """
    lazily build and cache a ``{hash(node): node}`` index for every node in
    ``corpus``'s tree, memoized on ``corpus`` itself; safe since the corpus
    tree is fully built once (``load_prompt_corpus_tree``) and never mutated
    afterward — avoids rescanning the whole tree on every ``resolve_node``
    call, which was previously O(n) per call (O(n^2) for a full tree walk)
    """
    cached = corpus.__dict__.get("_hash_index")
    if cached is None:
        cached = {hash(n): n for n in [corpus] + list(corpus.descendants)}
        corpus.__dict__["_hash_index"] = cached
    return cached


def _get_name_index(corpus):
    """
    same as :func:`_get_hash_index`, but keyed by node name; first match in
    preorder wins on duplicate names, matching the previous linear-scan
    behavior
    """
    cached = corpus.__dict__.get("_name_index")
    if cached is None:
        cached = {}
        for n in [corpus] + list(corpus.descendants):
            if n.name not in cached:
                cached[n.name] = n
        corpus.__dict__["_name_index"] = cached
    return cached


# Public API  ##################################################################
def resolve_node(corpus, node_arg):
    """
    search a node in ``corpus`` providing node object/name/hash

    (helper function used by ``PromptBlueprint``'s
    ``.checkmark()``, ``.uncheckmark()``, ``.is_checkmarked()``, and
    ``.__contains__()``)


    :param corpus: root of the corpus tree to search
    :type corpus: BasePromptNode
    :param node_arg: node object; hash value; name
    :type node_arg: BasePromptNode or int or str
    :raises TypeError:
    :raises ValueError:
    :return: the resolved node object and its hash value
    :rtype: tuple(BasePromptNode, int)
    """
    # search by name   ---------------------------------------------------------
    if isinstance(node_arg, str):
        node_obj = _get_name_index(corpus).get(node_arg)

        if node_obj is None:
            raise ValueError(
                "no node in corpus with name: {}".format(repr(node_arg))
            )

        node_hash = hash(node_obj)

    # search by node hash  -----------------------------------------------------
    elif isinstance(node_arg, int):
        node_obj = _get_hash_index(corpus).get(node_arg)

        if node_obj is None:
            raise ValueError(
                "no node in corpus with hash value: {}".format(repr(node_arg))
            )

        node_hash = node_arg

    # node is already object  --------------------------------------------------
    elif isinstance(node_arg, BasePromptNode):
        # root nodes all share the same (empty-lineage) hash, so a hash-index
        # lookup can't tell them apart — fall back to ``__eq__``'s full
        # tree-structural comparison, which only ever runs once per resolve
        # (roots are resolved once at the top of a tree walk, not per node)
        if node_arg.is_root:
            if node_arg != corpus:
                raise ValueError("node not in corpus: {}".format(node_arg))
            node_obj = node_arg
            node_hash = hash(node_arg)

        else:
            node_hash = hash(node_arg)

            if node_hash not in _get_hash_index(corpus):
                raise ValueError("node not in corpus: {}".format(node_arg))

            node_obj = node_arg

    else:
        raise TypeError(
            "must be BasePromptNode/int(hash value)/str(name): {}".format(
                node_arg
            )
        )

    return node_obj, node_hash
