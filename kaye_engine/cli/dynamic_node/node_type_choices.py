"""
node_type_choices.py

define ``NODE_TYPE_CHOICES``
"""

from kaye_engine.prompt.dynamic_nodes import TodayNode, AbbrNode

__all__ = ("NODE_TYPE_CHOICES",)

# constants  ###################################################################
# map CLI-facing NODE_TYPE identifiers to their engine-defined dynamic
# node class -- abbr group names are resolved separately, dynamically,
# see _resolve_node_type() in parser.py
NODE_TYPE_CHOICES = {
    "today": TodayNode,
    "abbr": AbbrNode,
}
