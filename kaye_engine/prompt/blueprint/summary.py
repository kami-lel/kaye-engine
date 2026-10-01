"""
summary.py

define ``BlueprintSummary``, ``show_blueprint``
"""

from dataclasses import dataclass

from .data import BlueprintMeta
from .render.meta import show_dependencies

__all__ = ("BlueprintSummary", "show_blueprint")


@dataclass(frozen=True, slots=True, kw_only=True)
class BlueprintSummary:
    """
    what a blueprint holds, at a glance


    :param meta: descriptors
    :type meta: BlueprintMeta
    :param node_count: how many nodes are checkmarked one by one
    :type node_count: int
    :param subtree_count: how many nodes are checkmarked together with
            their descendants
    :type subtree_count: int
    :param dependencies: see :func:`show_dependencies`
    :type dependencies: tuple[str, ...]
    """

    meta: BlueprintMeta
    node_count: int
    subtree_count: int
    dependencies: tuple[str, ...]


# Public API  ##################################################################
def show_blueprint(blueprint):
    """
    pure data: touches no corpus


    :param blueprint:
    :type blueprint: Blueprint
    :return: the summary of ``blueprint``'s meta, node counts, and
            dependencies
    :rtype: BlueprintSummary
    """
    return BlueprintSummary(
        meta=blueprint.meta,
        node_count=len(blueprint.nodes),
        subtree_count=len(blueprint.subtrees),
        dependencies=show_dependencies(blueprint),
    )
