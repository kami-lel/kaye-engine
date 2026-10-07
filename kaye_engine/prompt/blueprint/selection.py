"""
selection.py

define ``bind_selection`` and ``resolve_selection`` -- turn a
``Blueprint`` into the ``BlueprintSelection`` bitmask the renderers walk
"""

from ..prompt_corpus_loader import add_corpus_clear_hook
from .data import Blueprint
from .index import BlueprintSelection, get_corpus_index

__all__ = ("bind_selection", "resolve_selection")

# bound selections by blueprint; equal blueprints share one entry
_bound_selections = {}


# auxiliaries  #################################################################
def _drop_bound_selections():
    _bound_selections.clear()


add_corpus_clear_hook(_drop_bound_selections)


def _lookup_path_idx(index, path):
    try:
        return index.idx_by_path[path]
    except KeyError as err:
        raise ValueError(
            "no node in corpus at path: {}".format(list(path))
        ) from err


def _bind_own_mask(index, blueprint):
    """
    :return: bit mask of ``blueprint``'s own ``nodes`` and ``subtrees``,
            no dependencies; root and, under a subtree, sidecars are
            never selected
    :rtype: int
    """
    sidecars = 0
    for mask in index.sidecar_masks.values():
        sidecars |= mask

    mask = 0
    for path in blueprint.nodes:
        mask |= 1 << _lookup_path_idx(index, path)

    for path in blueprint.subtrees:
        mask |= index.subtree_masks[_lookup_path_idx(index, path)] & ~sidecars

    # root is only a container: it has no heading of its own to render
    return mask & ~1


def _resolve_mask(index, blueprint, stack):
    """
    :param stack: names of the registered blueprints being resolved, the
            cycle guard
    :type stack: tuple[str, ...]
    """
    from .registry import blueprint_registry  # pylint: disable=C0415

    mask = bind_selection(blueprint).mask

    for dep in blueprint.dependencies:
        if isinstance(dep, Blueprint):
            mask |= _resolve_mask(index, dep, stack)
            continue

        if dep in stack:
            raise ValueError(
                "dependency cycle detected at blueprint: {}".format(dep)
            )

        try:
            entry = blueprint_registry[dep]
        except KeyError as err:
            raise ValueError(
                "no blueprint registered under name: {}".format(dep)
            ) from err

        mask |= _resolve_mask(index, entry.blueprint, (*stack, dep))

    return mask


# Public API  ##################################################################
def bind_selection(blueprint):
    """
    Prerequisite: :func:`load_corpus_tree` called


    :param blueprint:
    :type blueprint: Blueprint
    :raises ValueError: no corpus is loaded, or a ``nodes`` or
            ``subtrees`` path names no node of it
    :return: the nodes ``blueprint`` itself selects, dependencies
            excluded; memoized until :func:`clear_corpus_tree`
    :rtype: BlueprintSelection
    """
    index = get_corpus_index()

    selection = _bound_selections.get(blueprint)
    if selection is None:
        selection = BlueprintSelection(index, _bind_own_mask(index, blueprint))
        _bound_selections[blueprint] = selection

    return selection


def resolve_selection(blueprint):
    """
    bind ``blueprint`` and OR in every transitive dependency; a dependency
    named by a ``str`` is looked up in ``blueprint_registry`` now, so one
    registered after its dependent, or replaced since, is seen


    :param blueprint:
    :type blueprint: Blueprint
    :raises ValueError: a dependency cycle, a dependency name that is not
            registered, or any error of :func:`bind_selection`
    :return: the nodes ``blueprint`` and its dependencies select
    :rtype: BlueprintSelection
    """
    index = get_corpus_index()

    return BlueprintSelection(index, _resolve_mask(index, blueprint, ()))
