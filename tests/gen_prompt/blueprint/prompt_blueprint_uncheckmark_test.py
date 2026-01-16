"""
prompt_blueprint_uncheckmark_test.py

Unit Tests (using pytest) for: PromptBlueprint

- .uncheckmark()
- __isub__()
"""

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


class Test1:  # corpus1  #######################################################

    corpus = PromptCorpusNode.parse(PROMPT1)

    # full -> partial 1  -------------------------------------------------------
    def test1_uncheckmark_by_obj(self):
        bp_text = BLUEPRINT_1_FULL
        opt = PromptBlueprint.parse(self.corpus, bp_text, disable_prune=True)
        _print_heading("before uncheckmark")
        print(opt)

        node = self.corpus["Project Title"]
        opt.uncheckmark(node)

        _print_heading("after uncheckmark")
        print(opt)

        assert (
            opt.generate_preview_tree(preview_line_count=0, hide_comment=True)
            == BLUEPRINT_1_PARTIAL_1
        )

    def test1_uncheckmark_by_hash(self):
        bp_text = BLUEPRINT_1_FULL
        opt = PromptBlueprint.parse(self.corpus, bp_text, disable_prune=True)
        _print_heading("before uncheckmark")
        print(opt)

        node = self.corpus["Project Title"]
        node_hash = hash(node)
        opt.uncheckmark(node_hash)

        _print_heading("after uncheckmark")
        print(opt)

        assert (
            opt.generate_preview_tree(preview_line_count=0, hide_comment=True)
            == BLUEPRINT_1_PARTIAL_1
        )

    def test1_isub_by_obj(self):
        bp_text = BLUEPRINT_1_FULL
        opt = PromptBlueprint.parse(self.corpus, bp_text, disable_prune=True)
        _print_heading("before uncheckmark")
        print(opt)

        node = self.corpus["Project Title"]
        opt -= node

        _print_heading("after uncheckmark")
        print(opt)

        assert (
            opt.generate_preview_tree(preview_line_count=0, hide_comment=True)
            == BLUEPRINT_1_PARTIAL_1
        )

    def test1_isub_by_hash(self):
        bp_text = BLUEPRINT_1_FULL
        opt = PromptBlueprint.parse(self.corpus, bp_text, disable_prune=True)
        _print_heading("before uncheckmark")
        print(opt)

        node = self.corpus["Project Title"]
        node_hash = hash(node)
        opt -= node_hash

        _print_heading("after uncheckmark")
        print(opt)

        assert (
            opt.generate_preview_tree(preview_line_count=0, hide_comment=True)
            == BLUEPRINT_1_PARTIAL_1
        )

    # full -> partial 2  -------------------------------------------------------
    def test2_uncheckmark_by_obj(self):
        bp_text = BLUEPRINT_1_FULL
        opt = PromptBlueprint.parse(self.corpus, bp_text, disable_prune=True)
        _print_heading("before uncheckmark")
        print(opt)

        node = self.corpus["Project Title"]["Description"]
        opt.uncheckmark(node)

        _print_heading("after uncheckmark")
        print(opt)

        assert (
            opt.generate_preview_tree(preview_line_count=0, hide_comment=True)
            == BLUEPRINT_1_PARTIAL_2
        )

    def test2_uncheckmark_by_hash(self):
        bp_text = BLUEPRINT_1_FULL
        opt = PromptBlueprint.parse(self.corpus, bp_text, disable_prune=True)
        _print_heading("before uncheckmark")
        print(opt)

        node = self.corpus["Project Title"]["Description"]
        node_hash = hash(node)
        opt.uncheckmark(node_hash)

        _print_heading("after uncheckmark")
        print(opt)

        assert (
            opt.generate_preview_tree(preview_line_count=0, hide_comment=True)
            == BLUEPRINT_1_PARTIAL_2
        )

    # err handling  ------------------------------------------------------------
    # TODO more tests


class Test2:  # PROMPT 2  ######################################################

    corpus = PromptCorpusNode.parse(PROMPT2)

    # full -> partial 1  -------------------------------------------------------
    def test1_uncheckmark_by_obj(self):
        bp_text = BLUEPRINT_2_FULL
        opt = PromptBlueprint.parse(self.corpus, bp_text, disable_prune=True)
        _print_heading("before uncheckmark")
        print(opt)

        proj_node = self.corpus["Project Title"]
        opt.uncheckmark(proj_node["Description"]).uncheckmark(
            proj_node["Usage"]
        ).uncheckmark(proj_node["License"])

        _print_heading("after uncheckmark")
        print(opt)

        assert (
            opt.generate_preview_tree(preview_line_count=0, hide_comment=True)
            == BLUEPRINT_2_PARTIAL_1
        )

    def test1_uncheckmark_by_hash(self):
        bp_text = BLUEPRINT_2_FULL
        opt = PromptBlueprint.parse(self.corpus, bp_text, disable_prune=True)
        _print_heading("before uncheckmark")
        print(opt)

        proj_node = self.corpus["Project Title"]
        for h in [
            hash(proj_node[name])
            for name in ("Description", "Usage", "License")
        ]:
            opt.uncheckmark(h)

        _print_heading("after uncheckmark")
        print(opt)

        assert (
            opt.generate_preview_tree(preview_line_count=0, hide_comment=True)
            == BLUEPRINT_2_PARTIAL_1
        )


class Test3:  # PROMPT 3  ######################################################

    corpus = PromptCorpusNode.parse(PROMPT3)

    # full -> partial 1  -------------------------------------------------------
    def test1_uncheckmark_by_obj(self):
        bp_text = BLUEPRINT_3_FULL
        opt = PromptBlueprint.parse(self.corpus, bp_text, disable_prune=True)
        _print_heading("before uncheckmark")
        print(opt)

        node = self.corpus["Main Title"]["Methods"]
        opt.uncheckmark(node)
        node = node["Data Collection"]
        opt.uncheckmark(node)
        node = node["Tools Used"]
        opt.uncheckmark(node)
        node = node["Future Work"]
        opt.uncheckmark(node)

        _print_heading("after uncheckmark")
        print(opt)

        assert (
            opt.generate_preview_tree(preview_line_count=0, hide_comment=True)
            == BLUEPRINT_3_PARTIAL_1
        )

    def test1_uncheckmark_by_hash(self):
        bp_text = BLUEPRINT_3_FULL
        opt = PromptBlueprint.parse(self.corpus, bp_text, disable_prune=True)
        _print_heading("before uncheckmark")
        print(opt)

        node = self.corpus["Main Title"]["Methods"]
        opt.uncheckmark(hash(node))
        node = node["Data Collection"]
        opt.uncheckmark(hash(node))
        node = node["Tools Used"]
        opt.uncheckmark(hash(node))
        node = node["Future Work"]
        opt.uncheckmark(hash(node))

        _print_heading("after uncheckmark")
        print(opt)

        assert (
            opt.generate_preview_tree(preview_line_count=0, hide_comment=True)
            == BLUEPRINT_3_PARTIAL_1
        )

    # full -> partial 2  -------------------------------------------------------
    def test2_uncheckmark_by_obj(self):
        bp_text = BLUEPRINT_3_FULL
        opt = PromptBlueprint.parse(self.corpus, bp_text, disable_prune=True)
        _print_heading("before uncheckmark")
        print(opt)

        main_node = self.corpus["Main Title"]
        node = main_node["Introduction"]
        opt.uncheckmark(node)
        node = node["Background"]["Importance"]
        opt.uncheckmark(node)
        node = main_node["Methods"]
        opt.uncheckmark(node)
        node = node["Data Collection"]["Tools Used"]
        opt.uncheckmark(node)
        node = main_node["Conclusion"]
        opt.uncheckmark(node)

        _print_heading("after uncheckmark")
        print(opt)

        assert (
            opt.generate_preview_tree(preview_line_count=0, hide_comment=True)
            == BLUEPRINT_3_PARTIAL_2
        )

    def test2_uncheckmark_by_hash(self):
        bp_text = BLUEPRINT_3_FULL
        opt = PromptBlueprint.parse(self.corpus, bp_text, disable_prune=True)
        _print_heading("before uncheckmark")
        print(opt)

        main_node = self.corpus["Main Title"]
        node = main_node["Introduction"]
        opt.uncheckmark(hash(node))
        node = node["Background"]["Importance"]
        opt.uncheckmark(hash(node))
        node = main_node["Methods"]
        opt.uncheckmark(hash(node))
        node = node["Data Collection"]["Tools Used"]
        opt.uncheckmark(hash(node))
        node = main_node["Conclusion"]
        opt.uncheckmark(hash(node))

        _print_heading("after uncheckmark")
        print(opt)

        assert (
            opt.generate_preview_tree(preview_line_count=0, hide_comment=True)
            == BLUEPRINT_3_PARTIAL_2
        )
