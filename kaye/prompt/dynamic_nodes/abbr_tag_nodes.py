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


# FIXME FIXME refactor to use abstract class

# TODO query content include program terms meaning


class UsableAbbrNode(DynamicNode):  ############################################
    """
    dynamic node to provide **Usable Abbreviations**
    """

    # implement DynamicNode  ===================================================

    HEADING = "Usable Abbreviations"

    # implement BasePromptNode  ================================================

    def content_lines(self, **kwargs):
        lines = []
        for entry in AbbrData().abbrs:
            if AbbrTags.usable in entry.tags:
                lines.append(entry.as_md_list_entry())

        return lines


class LanguageCodeNode(DynamicNode):  ##########################################
    """
    dynamic node to provide **Languages Code**
    """

    # implement DynamicNode  ===================================================

    HEADING = "Languages Code"

    # implement BasePromptNode  ================================================

    def content_lines(self, **kwargs):
        lines = []
        for entry in AbbrData().abbrs:
            if AbbrTags.language_code in entry.tags:
                lines.append(entry.as_md_list_entry())

        return lines


class PLCNode(DynamicNode):  ###################################################
    """
    dynamic node to provide **Programming Languages Code**
    """

    # implement DynamicNode  ===================================================

    HEADING = "Programming Languages Code"

    # implement BasePromptNode  ================================================

    def content_lines(self, **kwargs):
        lines = []
        for entry in AbbrData().abbrs:
            if AbbrTags.programming_language_code in entry.tags:
                lines.append(entry.as_md_list_entry())

        return lines


class UnityEngineAbbrNode(DynamicNode):  #######################################
    """
    dynamic node to provide **Unity Engine Abbreviations**
    """

    # implement DynamicNode  ===================================================

    HEADING = "Unity Engine Abbreviations"

    # implement BasePromptNode  ================================================

    def content_lines(self, **kwargs):
        lines = []
        for entry in AbbrData().abbrs:
            if AbbrTags.unity_engine_abbr in entry.tags:
                lines.append(entry.as_md_list_entry())

        return lines
