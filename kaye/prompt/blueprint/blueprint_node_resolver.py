"""
blueprint_node_resolver.py

define ``resolve_node``
"""

from ..base_prompt_node import BasePromptNode

__all__ = ("resolve_node",)


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
    corpus_and_descendants = [corpus] + list(corpus.descendants)

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
