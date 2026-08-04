"""
abbr_tag_nodes.py

define abbreviation-tag-filtered node types
"""

from kaye_engine import LOGGER_NAME, kamilog
from kaye_engine.abbr_collection import AbbrTags, get_abbr_data
from .dynamic_node import DynamicNode

__all__ = (
    "gen_abbrs_content_lines",
    "UsableAbbrNode",
    "LanguageCodeNode",
    "PLCNode",
    "UnityEngineAbbrNode",
    "CodingTermsNode",
    "PlanStepByStepAbbrNode",
)

# logger  ######################################################################
logger = kamilog.getLogger(LOGGER_NAME)


def gen_abbrs_content_lines(abbr_tag):
    """
    render every ``get_abbr_data().abbrs`` entry matching ``abbr_tag``
    as a list of markdown list items; empty when the abbr data singleton
    is still empty


    :param abbr_tag: tag to filter entries by
    :type abbr_tag: AbbrTags
    :return: rendered markdown list items, one per matching entry
    :rtype: list[str]
    """
    abbr_data = get_abbr_data()
    if not abbr_data:
        logger.warning(
            "abbr data is empty, rendering {} with no abbr content".format(
                repr(abbr_tag)
            )
        )
        return []

    lines = []
    for entry in abbr_data.abbrs:
        if abbr_tag in entry.tags:
            lines.append(entry.as_md_list_entry())
    return lines


class _AbbrTagNodeBase(DynamicNode):  ##########################################
    # pylint: disable=abstract-method
    """
    abstract dynamic node that provides abbreviation entries matching
    a single ``ABBR_TAG`` from ``get_abbr_data().abbrs``
    """

    # abstract fields  ---------------------------------------------------------

    ABBR_TAG = None

    # implement BasePromptNode  ------------------------------------------------

    def content_lines(self, **kwargs):
        return self._preface + gen_abbrs_content_lines(self.ABBR_TAG)


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


class PlanStepByStepAbbrNode(
    _AbbrTagNodeBase
):  # =================================
    """
    dynamic node to provide **Plan Step By Step Abbreviations**
    """

    HEADING = "Plan Step By Step Abbreviations"  # implement DynamicNode
    ABBR_TAG = AbbrTags.plan_step_by_step_abbr  # implement AbbrTagNode
