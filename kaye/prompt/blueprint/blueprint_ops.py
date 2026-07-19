"""
blueprint_ops.py

define ``prune`` and ``merge``
"""

__all__ = ("prune", "merge")


# auxiliaries  #################################################################
def _add_all_unprunable_nodes_recursively(old_bp, pruned_bp, node):
    """
    recursively walk ``node``, and add necessary nodes from ``old_bp`` to
    ``pruned_bp``, such that trivial branches are pruned in the ``pruned_bp``

    (helper function used in ``prune()``)


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


# Public API  ##################################################################
def prune(blueprint):
    """
    :param blueprint:
    :type blueprint: PromptBlueprint
    :return: a **pruned** blueprint (of ``blueprint``)
            which is a minimum version
            that contains only branches with checkmarked nodes
    :rtype: PromptBlueprint
    """
    # create bp w/ nothing; type(blueprint) avoids importing PromptBlueprint
    # here, which would create a circular import with prompt_blueprint.py
    pruned_bp = type(blueprint)(
        display_name=blueprint.display_name, corpus_override=blueprint.corpus
    )

    _add_all_unprunable_nodes_recursively(
        blueprint, pruned_bp, blueprint.corpus
    )

    return pruned_bp


def merge(a, b):
    """
    create a new **merged** blueprint as union of checkmarked nodes


    :param a:
    :type a: PromptBlueprint
    :param b:
    :type b: PromptBlueprint
    :raises ValueError:
    :return: merged blueprint
    :rtype: PromptBlueprint
    """
    if a.corpus != b.corpus:
        raise ValueError("must merge blueprint of same prompt tree")

    # create keys of resulted blueprint
    keys = set(a.keys()) | set(b.keys())

    # create display_name
    display_name = "|".join(
        name for name in (a.display_name, b.display_name) if name
    )

    merged = type(a)(display_name=display_name, corpus_override=a.corpus)

    merged.sidecars = a.sidecars | b.sidecars

    for k in keys:
        merged[k] = a.is_checkmarked(k) or b.is_checkmarked(k)

    return merged
