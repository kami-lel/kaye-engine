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

__all__ = ("AbbrGroupNode", "gen_group_abbrs_content_lines")

# logger  ######################################################################
logger = kamilog.getLogger(LOGGER_NAME)


def gen_group_abbrs_content_lines(group_name, is_sorted=False):
    """
    :param is_sorted: sort by ascending priority, numbered list, if True
    :type is_sorted: bool, optional
    :return: markdown list items for ``group_name``'s entries;
            empty when the abbr data singleton is empty, or unknown group
    :rtype: list[str]
    """
    abbr_data = get_abbr_data()
    if not abbr_data:
        logger.error("abbr data is empty, rendering without any abbr")
        return []

    entries = abbr_data.groups.entries_for(group_name)
    if is_sorted:
        entries = sorted(entries, key=lambda entry: entry.priority)
        return [
            entry.as_md_list_entry(number=i)
            for i, entry in enumerate(entries, start=1)
        ]

    return [entry.as_md_list_entry() for entry in entries]


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

    def content_lines(self, is_sorted=False, **kwargs):
        return self._preface + gen_group_abbrs_content_lines(
            self.group_name, is_sorted=is_sorted
        )

    def __copy__(self):
        return type(self)(
            None, group_name=self.group_name, preface=self._preface
        )
