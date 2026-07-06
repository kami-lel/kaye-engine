"""
abbr_nodes.py

define abbreviations-related node types
"""

from kaye.abbr_collection import AbbrData
from .dynamic_node import DynamicNode

__all__ = ("AbbrNode",)


# TODO generate by priority, ie give all priority zero; or alt tag?


class AbbrNode(DynamicNode):  ##################################################
    """
    dynamic node to provide abbreviations' meanings
    based on a given ``query`` content
    """

    # implement DynamicNode  ===================================================

    HEADING = "Abbreviations"

    # implement BasePromptNode  ================================================

    def content_lines(self, *, query=""):  # pylint: disable=arguments-differ
        # find abbr occurrences  -----------------------------------------------
        query_lower = query.lower()  # provide lower case to automation
        query_len = len(query)
        entries = set()

        for last_idx, matched in AbbrData().automaton.iter_long(query_lower):
            key_len = len(matched[0].abbr)
            end_idx = last_idx + 1
            start_idx = end_idx - key_len
            # get found text & its surrounding from original query
            found = query[start_idx:end_idx]
            char_before = query[start_idx - 1] if start_idx > 0 else ""
            char_after = query[end_idx] if end_idx < query_len else ""

            # check found satisfies additional rules
            for m in matched:
                if m.verify_found(found, char_before, char_after):
                    entries.add(m)

        # convert to md lines  -------------------------------------------------
        lines = [e.as_md_list_entry() for e in entries]
        return lines
