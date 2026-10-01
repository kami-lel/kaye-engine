"""
diff.py

define ``BlueprintDiff``, ``diff_blueprints``
"""

from typing import NamedTuple

from .data import Blueprint
from .index import NodePath

__all__ = ("BlueprintDiff", "diff_blueprints")


class BlueprintDiff(NamedTuple):
    """
    the nodes two blueprints do not share


    :param only_left: paths of ``nodes`` only the left blueprint holds
    :type only_left: frozenset[NodePath]
    :param only_right: paths of ``nodes`` only the right blueprint holds
    :type only_right: frozenset[NodePath]
    """

    only_left: frozenset[NodePath]
    only_right: frozenset[NodePath]


# Public API  ##################################################################
def diff_blueprints(left, right):
    """
    compare the checkmarked ``nodes`` of two blueprints; ``subtrees``,
    ``meta``, and ``dependencies`` take no part


    :param left:
    :type left: Blueprint
    :param right:
    :type right: Blueprint
    :return: the node paths only ``left`` holds, and only ``right`` holds
    :rtype: BlueprintDiff
    """
    return BlueprintDiff(
        only_left=left.nodes - right.nodes,
        only_right=right.nodes - left.nodes,
    )
