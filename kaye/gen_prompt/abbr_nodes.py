"""
define abbreviations-related node types
"""

from kaye.gen_prompt.abbr_collection import AbbrCollection
from kaye.gen_prompt.base_prompt_node import DynamicNode

__all__ = ("QueryAbbrNode", "PLCNode")


class QueryAbbrNode(DynamicNode):

    HEADING = "Abbreviations"

    # constructor  =============================================================

    def __init__(self, parent):
        super().__init__(self.HEADING, parent)

    # implement BasePromptNode  ================================================

    def content_lines(self, **kwargs):
        pass  # TODO TODO

    #     self.load_abbrs_json()
    #     query_lower = query.lower()

    #     lines = []
    #     for last_idx, entry in self._automaton.iter_long(query_lower):
    #         key_len = len(entry.key)
    #         end_idx = last_idx + 1
    #         start_idx = end_idx - key_len
    #         # get found text & its surrounding from original query
    #         found = query[start_idx:end_idx]
    #         char_before = query[start_idx - 1] if start_idx > 0 else ""
    #         char_after = query[end_idx] if end_idx > key_len else ""
    #         # check found satisfies additional rules
    #         if not entry.verify_found(found, char_before, char_after):
    #             continue  # skip this found

    #         line = "- {}:{}".format(entry.key, entry.mean)
    #         lines.append(line)

    #     return "\n".join(lines)


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
