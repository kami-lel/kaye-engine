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
    "CodingTermsNode",
)


class AbbrTagNodeBase(DynamicNode):  ###########################################
    # pylint: disable=abstract-method
    """
    abstract dynamic node that provides abbreviation entries matching
    a single ``ABBR_TAG`` from ``AbbrData().abbrs``
    """

    # Todo add preface

    # abstract property  -------------------------------------------------------

    ABBR_TAG = None

    # implement BasePromptNode  ------------------------------------------------

    def content_lines(self, **kwargs):
        lines = []
        for entry in AbbrData().abbrs:
            if self.ABBR_TAG in entry.tags:
                lines.append(entry.as_md_list_entry())
        return lines


# concrete classes  ############################################################

# Usage Cases  =================================================================


class UsableAbbrNode(AbbrTagNodeBase):  # **************************************
    """
    dynamic node to provide **Usable Abbreviations**
    """

    HEADING = "Usable Abbreviations"  # implement DynamicNode
    ABBR_TAG = AbbrTags.usable_in_brief  # implement AbbrTagNode


class CodingTermsNode(AbbrTagNodeBase):  # *************************************
    """
    dynamic node to provide **Coding/Programming Terms**
    """

    HEADING = "Coding Terms"  # implement DynamicNode
    ABBR_TAG = AbbrTags.coding  # implement AbbrTagNode


# specialized groups  ==========================================================


class PLCNode(AbbrTagNodeBase):  # *********************************************
    """
    dynamic node to provide **Programming Languages Code**
    """

    HEADING = "Programming Languages Code"  # implement DynamicNode
    ABBR_TAG = AbbrTags.programming_language_code  # implement AbbrTagNode


class LanguageCodeNode(AbbrTagNodeBase):  # ************************************
    """
    dynamic node to provide **Languages Code**
    """

    HEADING = "Languages Code"  # implement DynamicNode
    ABBR_TAG = AbbrTags.language_code  # implement AbbrTagNode


class UnityEngineAbbrNode(AbbrTagNodeBase):  # =================================
    """
    dynamic node to provide **Unity Engine Abbreviations**
    """

    HEADING = "Unity Engine Abbreviations"  # implement DynamicNode
    ABBR_TAG = AbbrTags.unity_engine_abbr  # implement AbbrTagNode
