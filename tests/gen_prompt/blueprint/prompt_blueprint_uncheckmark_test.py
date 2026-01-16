"""
prompt_blueprint_uncheckmark_test.py

Unit Tests (using pytest) for: PromptBlueprint.remove()
"""

from kaye.gen_prompt import PromptCorpusNode, PromptBlueprint
from tests.gen_prompt import PROMPT1, PROMPT2, PROMPT3
from tests.gen_prompt.blueprint import (
    BLUEPRINT_1_FULL,
    BLUEPRINT_1_PARTIAL_1,
    BLUEPRINT_1_PARTIAL_2,
    BLUEPRINT_1_PARTIAL_2_PRUNED,
    _print_heading,
)


class Test1:  # use corpus1  ###################################################

    corpus = PromptCorpusNode.parse(PROMPT1)

    # full -> partial 1  -------------------------------------------------------
    def test1_use_obj(self):
        bp_text = BLUEPRINT_1_FULL
        opt = PromptBlueprint.parse(self.corpus, bp_text, disable_prune=True)
        _print_heading("before uncheckmark")
        print(opt)

        node = self.corpus["Project Title"]
        ret = opt.uncheckmark(node)

        _print_heading("after uncheckmark")
        print(opt)
        _print_heading("returned object")
        print(ret)

        assert (
            opt.generate_preview_tree(preview_line_count=0, hide_comment=True)
            == BLUEPRINT_1_PARTIAL_1
        )

        assert (
            ret.generate_preview_tree(preview_line_count=0, hide_comment=True)
            == BLUEPRINT_1_PARTIAL_1
        )

    def test1_use_hash(self):
        bp_text = BLUEPRINT_1_FULL
        opt = PromptBlueprint.parse(self.corpus, bp_text, disable_prune=True)
        _print_heading("before uncheckmark")
        print(opt)

        node = self.corpus["Project Title"]
        node_hash = hash(node)
        ret = opt.uncheckmark(node_hash)

        _print_heading("after uncheckmark")
        print(opt)
        _print_heading("returned object")
        print(ret)

        assert (
            opt.generate_preview_tree(preview_line_count=0, hide_comment=True)
            == BLUEPRINT_1_PARTIAL_1
        )

        assert (
            ret.generate_preview_tree(preview_line_count=0, hide_comment=True)
            == BLUEPRINT_1_PARTIAL_1
        )

    # full -> partial 2  -------------------------------------------------------
    def test2_use_obj(self):
        bp_text = BLUEPRINT_1_FULL
        opt = PromptBlueprint.parse(self.corpus, bp_text, disable_prune=True)
        _print_heading("before uncheckmark")
        print(opt)

        node = self.corpus["Project Title"]["Description"]
        ret = opt.uncheckmark(node)

        _print_heading("after uncheckmark")
        print(opt)
        _print_heading("returned object")
        print(ret)

        assert (
            opt.generate_preview_tree(preview_line_count=0, hide_comment=True)
            == BLUEPRINT_1_PARTIAL_2
        )

        assert (
            ret.generate_preview_tree(preview_line_count=0, hide_comment=True)
            == BLUEPRINT_1_PARTIAL_2_PRUNED
        )

    def test2_use_hash(self):
        bp_text = BLUEPRINT_1_FULL
        opt = PromptBlueprint.parse(self.corpus, bp_text, disable_prune=True)
        _print_heading("before uncheckmark")
        print(opt)

        node = self.corpus["Project Title"]["Description"]
        node_hash = hash(node)
        ret = opt.uncheckmark(node_hash)

        _print_heading("after uncheckmark")
        print(opt)
        _print_heading("returned object")
        print(ret)

        assert (
            opt.generate_preview_tree(preview_line_count=0, hide_comment=True)
            == BLUEPRINT_1_PARTIAL_2
        )

        assert (
            ret.generate_preview_tree(preview_line_count=0, hide_comment=True)
            == BLUEPRINT_1_PARTIAL_2_PRUNED
        )

    # err handling  ------------------------------------------------------------
    # TODO more tests


class Test2:  # use corpus2  ##############################################

    corpus = PromptCorpusNode.parse(PROMPT2)

    # full -> partial 1  -------------------------------------------------------


class Test3:  # use corpus3  ##############################################

    corpus = PromptCorpusNode.parse(PROMPT3)

    # full -> partial 1  -------------------------------------------------------
    # full -> partial 2  -------------------------------------------------------
