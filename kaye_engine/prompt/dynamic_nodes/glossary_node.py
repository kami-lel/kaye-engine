"""
glossary_node.py

define ``GlossaryNode`` -- unlike the fixed set of dynamic node types in
``DYNAMIC_NODE_TYPES``, one ``GlossaryNode`` instance is created per
consumer-defined glossary name known to ``abbr_glossary_registry``, not
registered here
"""

from kaye_engine import LOGGER_NAME, kamilog
from kaye_engine.abbr_collection import get_abbr_data
from kaye_engine.abbr_collection.abbr_glossary_registry import get_abbr_glossary

from .dynamic_node import DynamicNode

__all__ = ("GlossaryNode", "gen_glossary_content_lines")

# logger  ######################################################################
logger = kamilog.getLogger(LOGGER_NAME)


def gen_glossary_content_lines(
    glossary_name,
    is_sorted=None,
    uses_numbered_list=None,
    glossary_priority_threshold=None,
    disable_remark=None,
):
    """
    :param is_sorted: sort by ascending priority instead of insertion
            order; defaults to the glossary's registered ``is_sorted``
    :type is_sorted: bool, optional
    :param uses_numbered_list: render numbered markers instead of
            bullets; defaults to the glossary's registered
            ``uses_numbered_list``
    :type uses_numbered_list: bool, optional
    :param glossary_priority_threshold: exclude entries whose priority
            is greater than this value from rendering; ``None`` (the
            default) disables this filtering
    :type glossary_priority_threshold: int, optional
    :param disable_remark: omit the ``(...)`` remark suffix; defaults to
            the glossary's registered ``disable_remark``
    :type disable_remark: bool, optional
    :return: markdown list items for ``glossary_name``'s entries;
            empty when the abbr data singleton is empty
    :rtype: list[str]
    """
    abbr_data = get_abbr_data()
    if not abbr_data:
        logger.error("abbr data is empty, rendering without any abbr")
        return []

    reg = get_abbr_glossary(glossary_name)
    if is_sorted is None:
        is_sorted = reg.is_sorted
    if uses_numbered_list is None:
        uses_numbered_list = reg.uses_numbered_list
    if disable_remark is None:
        disable_remark = reg.disable_remark

    entries = tuple(
        entry
        for entry in abbr_data.abbrs
        if glossary_name in entry.glossaries
    )
    if glossary_priority_threshold is not None:
        entries = tuple(
            entry
            for entry in entries
            if entry.priority <= glossary_priority_threshold
        )
    if is_sorted:
        entries = sorted(entries, key=lambda entry: entry.priority)

    if uses_numbered_list:
        return [
            entry.as_md_list_entry(number=i, disable_remark=disable_remark)
            for i, entry in enumerate(entries, start=1)
        ]

    return [
        entry.as_md_list_entry(disable_remark=disable_remark)
        for entry in entries
    ]


class GlossaryNode(DynamicNode):  ##############################################
    """
    dynamic node that provides every abbreviation entry belonging to a
    single, consumer-defined ``glossary_name`` -- ``glossaries`` on
    ``abbrs.json`` entries is free-form, so unlike every other dynamic
    node type this one is parametrized at construction time rather than
    by subclassing
    """

    def __init__(self, parent=None, *, glossary_name, preface=(), **kwargs):
        self.glossary_name = glossary_name
        self.NAME = glossary_name  # implement DynamicNode
        super().__init__(parent, preface=preface, **kwargs)

    # implement BasePromptNode  ------------------------------------------------

    def content_lines(
        self,
        is_sorted=None,
        uses_numbered_list=None,
        glossary_priority_threshold=None,
        disable_remark=None,
        **kwargs
    ):
        return self._preface + gen_glossary_content_lines(
            self.glossary_name,
            is_sorted=is_sorted,
            uses_numbered_list=uses_numbered_list,
            glossary_priority_threshold=glossary_priority_threshold,
            disable_remark=disable_remark,
        )

    def __copy__(self):
        return type(self)(
            None, glossary_name=self.glossary_name, preface=self._preface
        )
