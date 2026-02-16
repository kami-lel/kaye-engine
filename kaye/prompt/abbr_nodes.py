"""
define abbreviations-related node types
"""

from kaye.prompt.abbr_collection import AbbrData, AbbrTags
from kaye.prompt.base_prompt_node import DynamicNode

__all__ = ("AbbrNode", "PLCNode")


class AbbrNode(DynamicNode):
    """
    dynamic node to provide abbreviations' meanings
    based on a given ``query`` content
    """

    HEADING = "Abbreviations"

    # constructor  =============================================================

    def __init__(self, parent):
        super().__init__(self.HEADING, parent)

    # implement BasePromptNode  ================================================

    def content_lines(self, *, query=""):  # pylint: disable=arguments-differ
        # todo contextual abbrs eg: mb only applies when role kyc

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
        lines = ["- {}:{}".format(e.abbr, e.mean) for e in entries]
        return lines

    def __copy__(self):
        return AbbrNode(None)


class PLCNode(DynamicNode):
    """
    dynamic node to provide **Programming Languages Code**
    """

    HEADING = "Programming Languages Code"

    # constructor  =============================================================

    def __init__(self, parent):
        super().__init__(self.HEADING, parent)

    # implement BasePromptNode  ================================================

    def content_lines(self, **kwargs):
        lines = []
        for entry in AbbrData().abbrs:
            if AbbrTags.programming_language_code in entry.tags:
                lines.append("-`{}`:{}".format(entry.abbr, entry.mean))

        return lines

    def __copy__(self):
        return PLCNode(None)


# TODO usable abbreviations node
