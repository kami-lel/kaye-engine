"""
abbr_group_node.py

define ``AbbrGroupNode`` -- unlike the fixed set of dynamic node types in
``DYNAMIC_NODE_TYPES``, one ``AbbrGroupNode`` instance is created per
consumer-defined group name found in ``get_abbr_data().groups``, not
registered here
"""

from kaye_engine import LOGGER_NAME, kamilog
from kaye_engine.abbr_collection import get_abbr_data
from .dynamic_node import DynamicNode

__all__ = ("gen_group_abbrs_content_lines", "AbbrGroupNode")

# logger  ######################################################################
logger = kamilog.getLogger(LOGGER_NAME)


def gen_group_abbrs_content_lines(group_name):
    """
    render every ``get_abbr_data().groups`` entry matching ``group_name``
    as a list of markdown list items; empty when the abbr data singleton
    is still empty, or ``group_name`` is unknown


    :param group_name: group to filter entries by
    :type group_name: str
    :return: rendered markdown list items, one per matching entry
    :rtype: list[str]
    """
    abbr_data = get_abbr_data()
    if not abbr_data:
        logger.error("abbr data is empty, rendering without any abbr")
        return []

    return [
        entry.as_md_list_entry()
        for entry in abbr_data.groups.entries_for(group_name)
    ]


class AbbrGroupNode(DynamicNode):  #############################################
    """
    dynamic node that provides every abbreviation entry belonging to a
    single, consumer-defined ``group_name`` -- ``groups`` on ``abbrs.json``
    entries is free-form, so unlike every other dynamic node type this one
    is parametrized at construction time rather than by subclassing
    """

    def __init__(self, parent=None, *, group_name, preface=(), **kwargs):
        self.group_name = group_name
        self.HEADING = group_name  # implement DynamicNode
        super().__init__(parent, preface=preface, **kwargs)

    # implement BasePromptNode  ------------------------------------------------

    def content_lines(self, **kwargs):
        return self._preface + gen_group_abbrs_content_lines(self.group_name)

    def __copy__(self):
        return type(self)(
            None, group_name=self.group_name, preface=self._preface
        )
