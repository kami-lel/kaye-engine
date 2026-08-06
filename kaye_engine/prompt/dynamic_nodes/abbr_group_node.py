"""
abbr_group_node.py

define ``AbbrGroupNode`` -- unlike the fixed set of dynamic node types in
``DYNAMIC_NODE_TYPES``, one ``AbbrGroupNode`` instance is created per
consumer-defined group name known to ``abbr_group_registry``, not
registered here
"""

from kaye_engine import LOGGER_NAME, kamilog
from kaye_engine.abbr_collection import get_abbr_data
from kaye_engine.abbr_collection.abbr_group_registry import get_abbr_group

from .dynamic_node import DynamicNode

__all__ = ("AbbrGroupNode", "gen_group_abbrs_content_lines")

# logger  ######################################################################
logger = kamilog.getLogger(LOGGER_NAME)


def gen_group_abbrs_content_lines(group_name, is_sorted=None, uses_numbered_list=None):
    """
    :param is_sorted: sort by ascending priority instead of insertion
            order; defaults to the group's registered ``is_sorted``
    :type is_sorted: bool, optional
    :param uses_numbered_list: render numbered markers instead of
            bullets; defaults to the group's registered
            ``uses_numbered_list``
    :type uses_numbered_list: bool, optional
    :return: markdown list items for ``group_name``'s entries;
            empty when the abbr data singleton is empty
    :rtype: list[str]
    """
    abbr_data = get_abbr_data()
    if not abbr_data:
        logger.error("abbr data is empty, rendering without any abbr")
        return []

    reg = get_abbr_group(group_name)
    if is_sorted is None:
        is_sorted = reg.is_sorted
    if uses_numbered_list is None:
        uses_numbered_list = reg.uses_numbered_list

    entries = tuple(
        entry for entry in abbr_data.abbrs if group_name in entry.groups
    )
    if is_sorted:
        entries = sorted(entries, key=lambda entry: entry.priority)

    if uses_numbered_list:
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

    def content_lines(self, is_sorted=None, uses_numbered_list=None, **kwargs):
        return self._preface + gen_group_abbrs_content_lines(
            self.group_name,
            is_sorted=is_sorted,
            uses_numbered_list=uses_numbered_list,
        )

    def __copy__(self):
        return type(self)(
            None, group_name=self.group_name, preface=self._preface
        )
