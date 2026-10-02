"""
dependencies.py

define ``resolve_dependencies``, ``trace_dependencies``
"""

from .data import Blueprint

__all__ = ("resolve_dependencies", "trace_dependencies")


# auxiliaries  #################################################################
def _lookup_dependency(dep):
    """
    :param dep: a registered blueprint name, or a blueprint value
    :type dep: str or Blueprint
    :raises ValueError: ``dep`` is a name that is not registered
    :return: the blueprint ``dep`` stands for
    :rtype: Blueprint
    """
    from .registry import blueprint_registry  # pylint: disable=C0415

    if isinstance(dep, Blueprint):
        return dep

    try:
        return blueprint_registry[dep].blueprint
    except KeyError as err:
        raise ValueError(
            "no blueprint registered under name: {}".format(dep)
        ) from err


def _trace_into(blueprint, stack, ordered):
    """
    append every transitive dependency of ``blueprint`` to ``ordered``,
    each after its own dependencies and only once

    :param stack: names of the registered blueprints being traced, the
            cycle guard
    :type stack: tuple[str, ...]
    :param ordered: dependencies found so far, extended in place
    :type ordered: list[Blueprint]
    """
    for dep in blueprint.dependencies:
        if isinstance(dep, str) and dep in stack:
            raise ValueError(
                "dependency cycle detected at blueprint: {}".format(dep)
            )

        dep_blueprint = _lookup_dependency(dep)
        _trace_into(
            dep_blueprint,
            (*stack, dep) if isinstance(dep, str) else stack,
            ordered,
        )

        if dep_blueprint not in ordered:
            ordered.append(dep_blueprint)


# Public API  ##################################################################
def resolve_dependencies(blueprint):
    """
    turn the named dependencies of ``blueprint`` into values, looked up in
    ``blueprint_registry`` now; value dependencies pass through


    :param blueprint:
    :type blueprint: Blueprint
    :raises ValueError: a dependency name that is not registered
    :return: the direct dependencies as blueprint values, in order
    :rtype: tuple[Blueprint, ...]
    """
    return tuple(_lookup_dependency(dep) for dep in blueprint.dependencies)


def trace_dependencies(blueprint):
    """
    :param blueprint:
    :type blueprint: Blueprint
    :raises ValueError: a dependency cycle, or a dependency name that is
            not registered
    :return: the full transitive closure of ``blueprint``'s dependencies,
            ``blueprint`` itself excluded; each one follows its own
            dependencies and appears once
    :rtype: tuple[Blueprint, ...]
    """
    ordered = []
    _trace_into(blueprint, (), ordered)

    return tuple(ordered)
