"""
define abbreviations-related node types
"""

from kaye.gen_prompt.abbr_collection import AbbrCollection
from kaye.gen_prompt.base_prompt_node import DynamicNode

__all__ = ("AbbrNode", "PLCNode")


class AbbrNode(DynamicNode):

    HEADING = "Abbreviations"

    # constructor  =============================================================

    def __init__(self, parent):
        super().__init__(self.HEADING, parent)

    # implement BasePromptNode  ================================================

    def content_lines(self, **kwargs):
        if "query" not in kwargs:
            raise ValueError("must provide kwarg: query")
        query = kwargs["query"]

        # find abbr occurrences  -----------------------------------------------
        collection = AbbrCollection()
        query_lower = query.lower()  # provide lower case to automation
        query_len = len(query)
        entries = set()
        for last_idx, entry in collection.automaton.iter_long(query_lower):
            key_len = len(entry.key)
            end_idx = last_idx + 1
            start_idx = end_idx - key_len
            # get found text & its surrounding from original query
            found = query[start_idx:end_idx]
            char_before = query[start_idx - 1] if start_idx > 0 else ""
            char_after = query[end_idx] if end_idx < query_len else ""

            # BUG can't distinguish Cx/cx and Mx/mx
            # check found satisfies additional rules
            if entry.verify_found(found, char_before, char_after):
                entries.add(entry)

        # convert to md lines  -------------------------------------------------
        lines = ["- {}:{}".format(e.key, e.mean) for e in entries]
        return lines


class PLCNode(DynamicNode):

    HEADING = "Programming Languages Code"

    # constructor  =============================================================

    def __init__(self, parent):
        super().__init__(self.HEADING, parent)

    # implement BasePromptNode  ================================================
    def content_lines(self, **kwargs):
        lines = [""]
        for entry in AbbrCollection().generate_programming_languages_code():
            pass  # TODO

        return lines


# TODO usable abbrs node
