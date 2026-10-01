"""
edit.py

define the pure edit functions of ``Blueprint`` -- every one returns a
new blueprint and never mutates its argument:

- ``checkmark_nodes``, ``uncheckmark_nodes``, ``is_checkmarked``
- ``merge_blueprints``, ``replace_meta``
- ``create_blueprint_from_node``

a node argument is a node object, a node name, or a ``NodePath``
"""

import dataclasses

from ..base_prompt_node import BasePromptNode
from ..sidecar_node import get_sidecar_name
from .data import Blueprint, BlueprintMeta, create_blueprint
from .index import get_corpus_index

__all__ = (
    "checkmark_nodes",
    "create_blueprint_from_node",
    "is_checkmarked",
    "merge_blueprints",
    "replace_meta",
    "uncheckmark_nodes",
)

_META_NODE_FIELDS = ("description_node", "when_to_use_node", "globs_node")
_META_FIELDS = ("description", *_META_NODE_FIELDS)


# auxiliaries  #################################################################
def _resolve_path(node_arg):
    """
    :param node_arg: node object of the loaded corpus; node name (first
            match in pre-order); or ``NodePath``
    :type node_arg: BasePromptNode or str or tuple[str, ...]
    :raises TypeError: ``node_arg`` is none of the above (a hash integer
            is no longer one)
    :raises ValueError: no such node in the loaded corpus
    :return: the node's path
    :rtype: tuple[str, ...]
    """
    index = get_corpus_index()

    if isinstance(node_arg, BasePromptNode):
        path = tuple(node_arg.generate_lineage())
        idx = index.idx_by_path.get(path)
        if idx is None or index.node_objs[idx] is not node_arg:
            raise ValueError(
                "node does not belong to the loaded corpus: {}".format(node_arg)
            )
        return path

    if isinstance(node_arg, str):
        for idx, path in enumerate(index.paths):
            if path and path[-1] == node_arg:
                return path
        raise ValueError(
            "no node in corpus with name: {}".format(repr(node_arg))
        )

    if isinstance(node_arg, tuple) and all(
        isinstance(name, str) for name in node_arg
    ):
        if node_arg not in index.idx_by_path:
            raise ValueError(
                "no node in corpus at path: {}".format(list(node_arg))
            )
        return node_arg

    raise TypeError(
        "node must be a node object, a name, or a NodePath: {}".format(
            repr(node_arg)
        )
    )


def _resolve_optional_path(node_arg):
    return None if node_arg is None else _resolve_path(node_arg)


def _subtree_members(path):
    """
    :return: paths of the non-sidecar nodes a ``subtrees`` entry selects;
            root is never selected
    :rtype: set[tuple[str, ...]]
    """
    index = get_corpus_index()
    mask = index.subtree_masks[index.idx_by_path[path]]
    members = set()
    for idx, member_path in enumerate(index.paths):
        if (
            mask >> idx & 1
            and member_path
            and get_sidecar_name(index.node_objs[idx]) is None
        ):
            members.add(member_path)
    return members


def _is_under(path, ancestor):
    """
    :return: whether ``path`` is ``ancestor`` or lies beneath it
    :rtype: bool
    """
    return path[: len(ancestor)] == ancestor


def _expand_subtrees_covering(blueprint, path):
    """
    :return: ``blueprint`` with every ``subtrees`` entry that selects
            ``path`` replaced by the explicit ``nodes`` it selects
    :rtype: Blueprint
    """
    nodes = set(blueprint.nodes)
    subtrees = set(blueprint.subtrees)
    for entry in blueprint.subtrees:
        if _is_under(path, entry):
            members = _subtree_members(entry)
            if path in members:
                nodes |= members
                subtrees.discard(entry)
    return dataclasses.replace(
        blueprint, nodes=frozenset(nodes), subtrees=frozenset(subtrees)
    )


# Public API  ##################################################################
def is_checkmarked(blueprint, node):
    """
    :param blueprint:
    :type blueprint: Blueprint
    :param node: node object, name, or ``NodePath``
    :type node: BasePromptNode or str or tuple[str, ...]
    :raises TypeError:
    :raises ValueError: no such node in the loaded corpus
    :return: whether the blueprint's own ``nodes`` and ``subtrees`` select
            ``node``; dependencies are not consulted
    :rtype: bool
    """
    path = _resolve_path(node)

    if path in blueprint.nodes:
        return True

    return any(
        _is_under(path, entry) and path in _subtree_members(entry)
        for entry in blueprint.subtrees
    )


def checkmark_nodes(blueprint, node, *, is_recursive=False):
    """
    :param blueprint:
    :type blueprint: Blueprint
    :param node: node object, name, or ``NodePath``
    :type node: BasePromptNode or str or tuple[str, ...]
    :param is_recursive: whether to record ``node`` as a ``subtrees``
            entry, selecting every non-sidecar descendant too, even one
            added later
    :type is_recursive: bool, optional
    :raises TypeError:
    :raises ValueError: no such node in the loaded corpus
    :return: a new blueprint with ``node`` checkmarked
    :rtype: Blueprint
    """
    path = _resolve_path(node)

    if is_recursive:
        return dataclasses.replace(
            blueprint, subtrees=blueprint.subtrees | {path}
        )

    return dataclasses.replace(blueprint, nodes=blueprint.nodes | {path})


def uncheckmark_nodes(blueprint, node, *, is_recursive=False):
    """
    a subtree covering ``node`` is first expanded into explicit nodes, so
    only ``node`` (and, recursively, what lies beneath it) is removed;
    uncheckmarking a node that is not checkmarked changes nothing


    :param blueprint:
    :type blueprint: Blueprint
    :param node: node object, name, or ``NodePath``
    :type node: BasePromptNode or str or tuple[str, ...]
    :param is_recursive: whether to remove ``node`` and every ``nodes``
            and ``subtrees`` entry beneath it
    :type is_recursive: bool, optional
    :raises TypeError:
    :raises ValueError: no such node in the loaded corpus
    :return: a new blueprint with ``node`` unchecked
    :rtype: Blueprint
    """
    path = _resolve_path(node)

    if is_recursive:
        # entries at or beneath ``path`` all go; ancestors covering it
        # are expanded first so what they select outside it survives
        expanded = _expand_subtrees_covering(blueprint, path)
        return dataclasses.replace(
            expanded,
            nodes=frozenset(
                p for p in expanded.nodes if not _is_under(p, path)
            ),
            subtrees=frozenset(
                p for p in expanded.subtrees if not _is_under(p, path)
            ),
        )

    if not is_checkmarked(blueprint, path):
        return blueprint

    expanded = _expand_subtrees_covering(blueprint, path)
    return dataclasses.replace(expanded, nodes=expanded.nodes - {path})


def merge_blueprints(left, right):
    """
    :param left: wins every meta field it sets
    :type left: Blueprint
    :param right:
    :type right: Blueprint
    :return: union of both blueprints' ``nodes`` and ``subtrees``;
            dependencies of ``left`` then those of ``right`` not already
            present
    :rtype: Blueprint
    """
    meta = BlueprintMeta(
        **{
            field: (
                getattr(left.meta, field)
                if getattr(left.meta, field) is not None
                else getattr(right.meta, field)
            )
            for field in _META_FIELDS
        }
    )

    dependencies = list(left.dependencies)
    for dep in right.dependencies:
        if dep not in dependencies:
            dependencies.append(dep)

    return Blueprint(
        meta=meta,
        nodes=left.nodes | right.nodes,
        subtrees=left.subtrees | right.subtrees,
        dependencies=tuple(dependencies),
    )


def replace_meta(blueprint, **changes):
    """
    :param blueprint:
    :type blueprint: Blueprint
    :param changes: any of ``description``, ``description_node``,
            ``when_to_use_node``, ``globs_node``; ``None`` clears one; a
            node field takes a node object, name, or ``NodePath``
    :raises TypeError: an unknown field
    :raises ValueError: a node field names no node in the loaded corpus
    :return: a new blueprint with those meta fields replaced
    :rtype: Blueprint
    """
    unknown = set(changes) - set(_META_FIELDS)
    if unknown:
        raise TypeError(
            "unknown meta field: {}".format(", ".join(sorted(unknown)))
        )

    resolved = {
        field: (
            _resolve_optional_path(value)
            if field in _META_NODE_FIELDS
            else value
        )
        for field, value in changes.items()
    }

    return dataclasses.replace(
        blueprint, meta=dataclasses.replace(blueprint.meta, **resolved)
    )


def create_blueprint_from_node(
    node, *, is_recursive=False, meta=None, dependencies=()
):
    """
    :param node: node object, name, or ``NodePath``
    :type node: BasePromptNode or str or tuple[str, ...]
    :param is_recursive: whether to select its descendants too
    :type is_recursive: bool, optional
    :param meta: descriptors; defaults to none set
    :type meta: BlueprintMeta, optional
    :param dependencies: registered blueprint names or blueprint values
    :type dependencies: Iterable[str or Blueprint], optional
    :raises TypeError:
    :raises ValueError: no such node in the loaded corpus
    :return: a blueprint selecting ``node``
    :rtype: Blueprint
    """
    return checkmark_nodes(
        create_blueprint(meta=meta, dependencies=dependencies),
        node,
        is_recursive=is_recursive,
    )
