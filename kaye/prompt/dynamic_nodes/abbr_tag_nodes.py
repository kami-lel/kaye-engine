"""
abbr_tag_nodes.py

define abbreviation-tag-filtered node types
"""

from kaye.abbr_collection import AbbrData, AbbrTags
from .dynamic_node import DynamicNode

__all__ = (
    "UsableAbbrNode",
    "LanguageCodeNode",
    "PLCNode",
    "UnityEngineAbbrNode",
)


# simple abbr tag  #############################################################


class _SimpleAbbrTagNodeBase(DynamicNode):  # ==================================
    # pylint: disable=abstract-method
    """
    abstract dynamic node that provides abbreviation entries matching
    a single ``ABBR_TAG`` from ``AbbrData().abbrs``
    """

    # abstract property  -------------------------------------------------------

    ABBR_TAG = None

    # implement BasePromptNode  ------------------------------------------------

    def content_lines(self, **kwargs):
        lines = []
        for entry in AbbrData().abbrs:
            if self.ABBR_TAG in entry.tags:
                lines.append(entry.as_md_list_entry())
        return lines


class UsableAbbrNode(_SimpleAbbrTagNodeBase):  # ===============================
    """
    dynamic node to provide **Usable Abbreviations**
    """

    HEADING = "Usable Abbreviations"  # implement DynamicNode
    ABBR_TAG = AbbrTags.usable  # implement AbbrTagNode


class LanguageCodeNode(_SimpleAbbrTagNodeBase):  # =============================
    """
    dynamic node to provide **Languages Code**
    """

    HEADING = "Languages Code"  # implement DynamicNode
    ABBR_TAG = AbbrTags.language_code  # implement AbbrTagNode


class PLCNode(_SimpleAbbrTagNodeBase):  # ======================================
    """
    dynamic node to provide **Programming Languages Code**
    """

    HEADING = "Programming Languages Code"  # implement DynamicNode
    ABBR_TAG = AbbrTags.programming_language_code  # implement AbbrTagNode


class UnityEngineAbbrNode(_SimpleAbbrTagNodeBase):  # ==========================
    """
    dynamic node to provide **Unity Engine Abbreviations**
    """

    HEADING = "Unity Engine Abbreviations"  # implement DynamicNode
    ABBR_TAG = AbbrTags.unity_engine_abbr  # implement AbbrTagNode


# TODO TODO query content include program terms meaning with coding
