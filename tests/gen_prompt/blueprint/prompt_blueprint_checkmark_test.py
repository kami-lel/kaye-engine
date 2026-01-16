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


class Test11:  # PROMPT1: partial 1 -> full  ###################################

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

    def test1_iadd_by_obj(self):
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

    def test1_iadd_by_hash(self):
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
    def test_bad_type(self):
        bp_text = self.src
        opt = PromptBlueprint.parse(self.corpus, bp_text, disable_prune=True)

        with pytest.raises(TypeError) as exec_info:
            opt.checkmark(12.5)

        opt = exec_info.value.args[0]
        print(opt)

        assert opt == "must be PromptCorpusNode or hash value, not: 12.5"

    def test_bad_hash(self):
        bp_text = self.src
        opt = PromptBlueprint.parse(self.corpus, bp_text, disable_prune=True)

        with pytest.raises(ValueError) as exec_info:
            opt.checkmark(5)

        opt = exec_info.value.args[0]
        print(opt)

        assert opt == "node missing from blueprint's corpus: 5"

    def test_bad_obj(self):
        bp_text = self.src
        opt = PromptBlueprint.parse(self.corpus, bp_text, disable_prune=True)
        bad_node = PromptCorpusNode.parse(PROMPT3)["Main Title"]

        with pytest.raises(ValueError) as exec_info:
            opt.checkmark(bad_node)

        opt = exec_info.value.args[0]
        print(opt)

        assert (
            opt
            == "node missing from blueprint's corpus: "
            "PromptCorpusNode(Main Title)"
        )


class Test12:  # PROMPT 1: partial 2 -> full  ##################################

    corpus = PromptCorpusNode.parse(PROMPT1)
    src = BLUEPRINT_1_PARTIAL_2
    dest = BLUEPRINT_1_FULL

    def test2_checkmark_by_obj(self):
        bp_text = self.src
        opt = PromptBlueprint.parse(self.corpus, bp_text, disable_prune=True)
        _print_heading("before checkmark")
        print(opt)

        node = self.corpus["Project Title"]["Description"]
        opt.checkmark(node)

        _print_heading("after checkmark")
        print(opt)

        assert (
            opt.generate_preview_tree(preview_line_count=0, hide_comment=True)
            == self.dest
        )

    def test2_checkmark_by_hash(self):
        bp_text = self.src
        opt = PromptBlueprint.parse(self.corpus, bp_text, disable_prune=True)
        _print_heading("before checkmark")
        print(opt)

        node = self.corpus["Project Title"]["Description"]
        node_hash = hash(node)
        opt.checkmark(node_hash)

        _print_heading("after checkmark")
        print(opt)

        assert (
            opt.generate_preview_tree(preview_line_count=0, hide_comment=True)
            == self.dest
        )


class Test2:  # PROMPT2: full -> partial 1  ####################################

    corpus = PromptCorpusNode.parse(PROMPT2)
    src = BLUEPRINT_2_PARTIAL_1
    dest = BLUEPRINT_2_FULL

    def test1_checkmark_by_obj(self):
        bp_text = self.src
        opt = PromptBlueprint.parse(self.corpus, bp_text, disable_prune=True)
        _print_heading("before checkmark")
        print(opt)

        proj_node = self.corpus["Project Title"]
        opt.checkmark(proj_node["Description"]).checkmark(
            proj_node["Usage"]
        ).checkmark(proj_node["License"])

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

        proj_node = self.corpus["Project Title"]
        for h in [
            hash(proj_node[name])
            for name in ("Description", "Usage", "License")
        ]:
            opt.checkmark(h)

        _print_heading("after checkmark")
        print(opt)

        assert (
            opt.generate_preview_tree(preview_line_count=0, hide_comment=True)
            == self.dest
        )


class Test31:  # PROMPT3: partial 1 -> full  ###################################

    corpus = PromptCorpusNode.parse(PROMPT3)
    src = BLUEPRINT_3_PARTIAL_1
    dest = BLUEPRINT_3_FULL

    def test1_checkmark_by_obj(self):
        bp_text = self.src
        opt = PromptBlueprint.parse(self.corpus, bp_text, disable_prune=True)
        _print_heading("before checkmark")
        print(opt)

        node = self.corpus["Main Title"]["Methods"]
        opt.checkmark(node)
        node = node["Data Collection"]
        opt.checkmark(node)
        node = node["Tools Used"]
        opt.checkmark(node)
        node = node["Future Work"]
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

        node = self.corpus["Main Title"]["Methods"]
        opt.checkmark(hash(node))
        node = node["Data Collection"]
        opt.checkmark(hash(node))
        node = node["Tools Used"]
        opt.checkmark(hash(node))
        node = node["Future Work"]
        opt.checkmark(hash(node))

        _print_heading("after checkmark")
        print(opt)

        assert (
            opt.generate_preview_tree(preview_line_count=0, hide_comment=True)
            == self.dest
        )


class Test32:  # PROMPT3: partial 2 -> full  ###################################

    corpus = PromptCorpusNode.parse(PROMPT3)
    src = BLUEPRINT_3_PARTIAL_2
    dest = BLUEPRINT_3_FULL

    def test2_checkmark_by_obj(self):
        bp_text = self.src
        opt = PromptBlueprint.parse(self.corpus, bp_text, disable_prune=True)
        _print_heading("before checkmark")
        print(opt)

        main_node = self.corpus["Main Title"]
        node = main_node["Introduction"]
        opt.checkmark(node)
        node = node["Background"]["Importance"]
        opt.checkmark(node)
        node = main_node["Methods"]
        opt.checkmark(node)
        node = node["Data Collection"]["Tools Used"]
        opt.checkmark(node)
        node = main_node["Conclusion"]
        opt.checkmark(node)

        _print_heading("after checkmark")
        print(opt)

        assert (
            opt.generate_preview_tree(preview_line_count=0, hide_comment=True)
            == self.dest
        )

    def test2_checkmark_by_hash(self):
        bp_text = self.src
        opt = PromptBlueprint.parse(self.corpus, bp_text, disable_prune=True)
        _print_heading("before checkmark")
        print(opt)

        main_node = self.corpus["Main Title"]
        node = main_node["Introduction"]
        opt.checkmark(hash(node))
        node = node["Background"]["Importance"]
        opt.checkmark(hash(node))
        node = main_node["Methods"]
        opt.checkmark(hash(node))
        node = node["Data Collection"]["Tools Used"]
        opt.checkmark(hash(node))
        node = main_node["Conclusion"]
        opt.checkmark(hash(node))

        _print_heading("after checkmark")
        print(opt)

        assert (
            opt.generate_preview_tree(preview_line_count=0, hide_comment=True)
            == self.dest
        )
