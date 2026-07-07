"""
abbr_tag_nodes.py

define abbreviation-tag-filtered node types
"""

from kaye.abbr_collection import AbbrData, AbbrTags
from .dynamic_node import DynamicNode

__all__ = (
    "gen_abbrs_content_lines",
    "UsableAbbrNode",
    "LanguageCodeNode",
    "PLCNode",
    "UnityEngineAbbrNode",
    "CodingTermsNode",
)


def gen_abbrs_content_lines(abbr_tag):
    """
    render every ``AbbrData().abbrs`` entry matching ``abbr_tag``
    as a list of markdown list items


    :param abbr_tag: tag to filter entries by
    :type abbr_tag: AbbrTags
    :return: rendered markdown list items, one per matching entry
    :rtype: list[str]
    """
    lines = []
    for entry in AbbrData().abbrs:
        if abbr_tag in entry.tags:
            lines.append(entry.as_md_list_entry())
    return lines


class _AbbrTagNodeBase(DynamicNode):  ##########################################
    # pylint: disable=abstract-method
    """
    abstract dynamic node that provides abbreviation entries matching
    a single ``ABBR_TAG`` from ``AbbrData().abbrs``
    """

    # abstract property  -------------------------------------------------------

    ABBR_TAG = None

    # implement BasePromptNode  ------------------------------------------------

    def content_lines(self, **kwargs):
        # TODO add preface
        return gen_abbrs_content_lines(self.ABBR_TAG)


# concrete classes  ############################################################

# Usage Cases  =================================================================


class UsableAbbrNode(_AbbrTagNodeBase):  # *************************************
    """
    dynamic node to provide **Usable Abbreviations**
    """

    HEADING = "Usable Abbreviations"  # implement DynamicNode
    ABBR_TAG = AbbrTags.usable_in_brief  # implement AbbrTagNode


class CodingTermsNode(_AbbrTagNodeBase):  # ************************************
    """
    dynamic node to provide **Coding/Programming Terms**
    """

    HEADING = "Coding Terms"  # implement DynamicNode
    ABBR_TAG = AbbrTags.coding  # implement AbbrTagNode


# specialized groups  ==========================================================


class PLCNode(_AbbrTagNodeBase):  # ********************************************
    """
    dynamic node to provide **Programming Languages Code**
    """

    HEADING = "Programming Languages Code"  # implement DynamicNode
    ABBR_TAG = AbbrTags.programming_language_code  # implement AbbrTagNode


class LanguageCodeNode(_AbbrTagNodeBase):  # ***********************************
    """
    dynamic node to provide **Languages Code**
    """

    HEADING = "Languages Code"  # implement DynamicNode
    ABBR_TAG = AbbrTags.language_code  # implement AbbrTagNode


class UnityEngineAbbrNode(
    _AbbrTagNodeBase
):  # =================================
    """
    dynamic node to provide **Unity Engine Abbreviations**
    """

    HEADING = "Unity Engine Abbreviations"  # implement DynamicNode
    ABBR_TAG = AbbrTags.unity_engine_abbr  # implement AbbrTagNode
