"""
prompt_blueprint_checkmark_test.py

Unit Tests (using pytest) for: PromptBlueprint:

- .checkmark()
- .__iadd__()
"""

import pytest

from kaye.gen_prompt import PromptCorpusNode, PromptBlueprint
from tests.gen_prompt import PROMPT1, PROMPT2, PROMPT3
from tests.gen_prompt.blueprint import (
    BLUEPRINT_1_FULL,
    BLUEPRINT_1_PARTIAL_1,
    BLUEPRINT_1_PARTIAL_2,
    BLUEPRINT_2_FULL,
    BLUEPRINT_2_PARTIAL_1,
    BLUEPRINT_3_FULL,
    BLUEPRINT_3_PARTIAL_1,
    BLUEPRINT_3_PARTIAL_2,
    _print_heading,
)


class Test11:  # PROMPT1:  partial 1 -> full  ##################################

    corpus = PromptCorpusNode.parse(PROMPT1)
    src = BLUEPRINT_1_PARTIAL_1
    dest = BLUEPRINT_1_FULL

    def test1_checkmark_by_obj(self):
        bp_text = self.src
        opt = PromptBlueprint.parse(self.corpus, bp_text, disable_prune=True)
        _print_heading("before checkmark")
        print(opt)

        node = self.corpus["Project Title"]
        opt.checkmark(node)

        _print_heading("after checkmark")
        print(opt)

        assert (
            opt.generate_preview_tree(preview_line_count=0, hide_comment=True)
            == self.dest
        )

    def test1_checkmark_by_hash(self):
        bp_text = self.src
        opt = PromptBlueprint.parse(self.corpus, bp_text, disable_prune=True)
        _print_heading("before checkmark")
        print(opt)

        node = self.corpus["Project Title"]
        node_hash = hash(node)
        opt.checkmark(node_hash)

        _print_heading("after checkmark")
        print(opt)

        assert (
            opt.generate_preview_tree(preview_line_count=0, hide_comment=True)
            == self.dest
        )

    def test1_isub_by_obj(self):
        bp_text = self.src
        opt = PromptBlueprint.parse(self.corpus, bp_text, disable_prune=True)
        _print_heading("before checkmark")
        print(opt)

        node = self.corpus["Project Title"]
        opt += node

        _print_heading("after checkmark")
        print(opt)

        assert (
            opt.generate_preview_tree(preview_line_count=0, hide_comment=True)
            == self.dest
        )

    def test1_isub_by_hash(self):
        bp_text = self.src
        opt = PromptBlueprint.parse(self.corpus, bp_text, disable_prune=True)
        _print_heading("before checkmark")
        print(opt)

        node = self.corpus["Project Title"]
        node_hash = hash(node)
        opt += node_hash

        _print_heading("after checkmark")
        print(opt)

        assert (
            opt.generate_preview_tree(preview_line_count=0, hide_comment=True)
            == self.dest
        )

    # err handling  ------------------------------------------------------------
    # TODO
