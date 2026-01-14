"""
prompt_blueprint_parse_advanced_test.py

Unit Tests (using pytest) for: PromptBlueprint.parse()

this perform tests relied on
accurate implementation of PromptBlueprint.generate_preview_tree()
"""

from kaye.gen_prompt import PromptCorpusNode, PromptBlueprint
from tests.gen_prompt import PROMPT1, PROMPT2, PROMPT3
from tests.gen_prompt.blueprint import (
    BLUEPRINT_1_FULL,
    BLUEPRINT_1_FULL_PREVIEW,
    BLUEPRINT_1_PARTIAL_1,
    BLUEPRINT_1_PARTIAL_1_PREVIEW,
    BLUEPRINT_1_PARTIAL_2,
    BLUEPRINT_1_PARTIAL_2_PREVIEW,
    BLUEPRINT_1_PARTIAL_2_PRUNED,
    BLUEPRINT_1_EMPTY,
    BLUEPRINT_2_FULL,
    BLUEPRINT_2_PREVIEW,
    BLUEPRINT_2_PARTIAL_1,
    BLUEPRINT_2_PARTIAL_1_PREVIEW,
    BLUEPRINT_2_PARTIAL_1_PRUNED,
    BLUEPRINT_2_EMPTY,
    BLUEPRINT_3_FULL,
    BLUEPRINT_3_FULL_PREVIEW,
    BLUEPRINT_3_PARTIAL_1,
    BLUEPRINT_3_PARTIAL_1_PREVIEW,
    BLUEPRINT_3_PARTIAL_1_PRUNED,
    BLUEPRINT_3_PARTIAL_2,
    BLUEPRINT_3_PARTIAL_2_PREVIEW,
    BLUEPRINT_3_PARTIAL_2_PRUNED,
    BLUEPRINT_3_EMPTY,
    BLUEPRINT_EMPTY_PRUNED,
)

CORPUS1 = PromptCorpusNode.parse(PROMPT1)
CORPUS2 = PromptCorpusNode.parse(PROMPT2)
CORPUS3 = PromptCorpusNode.parse(PROMPT3)


# default behavior  ############################################################
class TestDft1:  # use PROMPT1  ==============================================

    corpus = CORPUS1

    def test_full(self):
        bp_text = BLUEPRINT_1_FULL

        opt = PromptBlueprint.parse(self.corpus, bp_text)

        print(opt)
        assert isinstance(opt, PromptBlueprint)
        assert len(opt) == 4
        assert opt.corpus is self.corpus
        assert opt.display_name == ""
        assert (
            opt.generate_preview_tree(preview_line_count=0, hide_comment=True)
            == bp_text
        )

    def test_part1(self):
        bp_text = BLUEPRINT_1_PARTIAL_1

        opt = PromptBlueprint.parse(self.corpus, bp_text)

        print(opt)
        assert len(opt) == 4
        assert (
            opt.generate_preview_tree(preview_line_count=0, hide_comment=True)
            == bp_text
        )

    def test_part2(self):
        bp_text = BLUEPRINT_1_PARTIAL_2

        opt = PromptBlueprint.parse(self.corpus, bp_text)

        print(opt)
        assert len(opt) == 3
        assert (
            opt.generate_preview_tree(preview_line_count=0, hide_comment=True)
            == BLUEPRINT_1_PARTIAL_2_PRUNED
        )

    def test_empty(self):
        bp_text = BLUEPRINT_1_EMPTY

        opt = PromptBlueprint.parse(self.corpus, bp_text)

        print(opt)
        assert len(opt) == 0
        assert (
            opt.generate_preview_tree(preview_line_count=0, hide_comment=True)
            == BLUEPRINT_EMPTY_PRUNED
        )


class TestDft2:  # use PROMPT2  ================================================

    corpus = CORPUS2

    def test_full(self):
        bp_text = BLUEPRINT_2_FULL

        opt = PromptBlueprint.parse(self.corpus, bp_text)

        print(opt)
        assert isinstance(opt, PromptBlueprint)
        assert len(opt) == 6
        assert opt.corpus is self.corpus
        assert opt.display_name == ""
        assert (
            opt.generate_preview_tree(preview_line_count=0, hide_comment=True)
            == bp_text
        )

    def test_part1(self):
        bp_text = BLUEPRINT_2_PARTIAL_1

        opt = PromptBlueprint.parse(self.corpus, bp_text)

        print(opt)
        assert len(opt) == 3
        assert (
            opt.generate_preview_tree(preview_line_count=0, hide_comment=True)
            == BLUEPRINT_2_PARTIAL_1_PRUNED
        )

    def test_empty(self):
        bp_text = BLUEPRINT_2_EMPTY

        opt = PromptBlueprint.parse(self.corpus, bp_text)

        print(opt)
        assert len(opt) == 0
        assert (
            opt.generate_preview_tree(preview_line_count=0, hide_comment=True)
            == BLUEPRINT_EMPTY_PRUNED
        )


class TestDft3:  # use PROMPT3  ================================================

    corpus = CORPUS3

    def test_full(self):
        bp_text = BLUEPRINT_3_FULL

        opt = PromptBlueprint.parse(self.corpus, bp_text)

        print(opt)
        assert isinstance(opt, PromptBlueprint)
        assert len(opt) == 10
        assert opt.corpus is self.corpus
        assert opt.display_name == ""
        assert (
            opt.generate_preview_tree(preview_line_count=0, hide_comment=True)
            == bp_text
        )

    def test_part1(self):
        bp_text = BLUEPRINT_3_PARTIAL_1

        opt = PromptBlueprint.parse(self.corpus, bp_text)

        print(opt)
        assert len(opt) == 6
        assert (
            opt.generate_preview_tree(preview_line_count=0, hide_comment=True)
            == BLUEPRINT_3_PARTIAL_1_PRUNED
        )

    def test_part2(self):
        bp_text = BLUEPRINT_3_PARTIAL_2
        opt = PromptBlueprint.parse(self.corpus, bp_text)

        print(opt)
        assert len(opt) == 9
        assert (
            opt.generate_preview_tree(preview_line_count=0, hide_comment=True)
            == BLUEPRINT_3_PARTIAL_2_PRUNED
        )

    def test_empty(self):
        bp_text = BLUEPRINT_3_EMPTY
        opt = PromptBlueprint.parse(self.corpus, bp_text)

        print(opt)
        assert len(opt) == 0
        assert (
            opt.generate_preview_tree(preview_line_count=0, hide_comment=True)
            == BLUEPRINT_EMPTY_PRUNED
        )


# text include content preview  ################################################
class TestContentPreview1:  # use PROMPT1  =====================================

    def test1(_):
        bp_text = BLUEPRINT_1_FULL_PREVIEW

        opt = PromptBlueprint.parse(CORPUS1, bp_text)

        print(opt)
        assert (
            opt.generate_preview_tree(preview_line_count=0, hide_comment=True)
            == BLUEPRINT_1_FULL
        )

    def test_pa1(_):
        bp_text = BLUEPRINT_1_PARTIAL_1_PREVIEW

        opt = PromptBlueprint.parse(CORPUS1, bp_text)

        print(opt)
        assert (
            opt.generate_preview_tree(preview_line_count=0, hide_comment=True)
            == BLUEPRINT_1_PARTIAL_1
        )

    def test_pa2(_):
        bp_text = BLUEPRINT_1_PARTIAL_2_PREVIEW

        opt = PromptBlueprint.parse(CORPUS1, bp_text)

        print(opt)
        assert (
            opt.generate_preview_tree(preview_line_count=0, hide_comment=True)
            == BLUEPRINT_1_PARTIAL_2_PRUNED
        )


class TestContentPreview2:  # use PROMPT2  =====================================

    def test_full(_):
        bp_text = BLUEPRINT_2_PREVIEW

        opt = PromptBlueprint.parse(CORPUS2, bp_text)

        print(opt)
        assert (
            opt.generate_preview_tree(preview_line_count=0, hide_comment=True)
            == BLUEPRINT_2_FULL
        )

    def test_pa1(_):
        bp_text = BLUEPRINT_2_PARTIAL_1_PREVIEW

        opt = PromptBlueprint.parse(CORPUS2, bp_text)

        print(opt)
        assert (
            opt.generate_preview_tree(preview_line_count=0, hide_comment=True)
            == BLUEPRINT_2_PARTIAL_1_PRUNED
        )


class TestContentPreview3:  # use PROMPT2  =====================================

    def test_full(_):
        bp_text = BLUEPRINT_3_FULL_PREVIEW

        opt = PromptBlueprint.parse(CORPUS3, bp_text)

        print(opt)
        assert (
            opt.generate_preview_tree(preview_line_count=0, hide_comment=True)
            == BLUEPRINT_3_FULL
        )

    def test_pa1(_):
        bp_text = BLUEPRINT_3_PARTIAL_1_PREVIEW

        opt = PromptBlueprint.parse(CORPUS3, bp_text)

        print(opt)
        assert (
            opt.generate_preview_tree(preview_line_count=0, hide_comment=True)
            == BLUEPRINT_3_PARTIAL_1_PRUNED
        )

    def test_pa2(_):
        bp_text = BLUEPRINT_3_PARTIAL_2_PREVIEW

        opt = PromptBlueprint.parse(CORPUS3, bp_text)

        print(opt)
        assert (
            opt.generate_preview_tree(preview_line_count=0, hide_comment=True)
            == BLUEPRINT_3_PARTIAL_2_PRUNED
        )


# blueprint text is pruned  ####################################################
class TestPrunedText:

    def test1(_):
        bp_text = BLUEPRINT_1_PARTIAL_2_PRUNED

        opt = PromptBlueprint.parse(CORPUS1, bp_text)

        print(opt)
        assert (
            opt.generate_preview_tree(preview_line_count=0, hide_comment=True)
            == bp_text
        )

    def test2(_):
        bp_text = BLUEPRINT_2_PARTIAL_1_PRUNED

        opt = PromptBlueprint.parse(CORPUS2, bp_text)

        print(opt)
        assert (
            opt.generate_preview_tree(preview_line_count=0, hide_comment=True)
            == bp_text
        )

    def test31(_):
        bp_text = BLUEPRINT_3_PARTIAL_1_PRUNED

        opt = PromptBlueprint.parse(CORPUS3, bp_text)

        print(opt)
        assert (
            opt.generate_preview_tree(preview_line_count=0, hide_comment=True)
            == bp_text
        )

    def test32(_):
        bp_text = BLUEPRINT_3_PARTIAL_2_PRUNED

        opt = PromptBlueprint.parse(CORPUS3, bp_text)

        print(opt)
        assert (
            opt.generate_preview_tree(preview_line_count=0, hide_comment=True)
            == bp_text
        )

    def test_pruned_input(_):
        bp_text = """    ○
[x] └── Main Title
[x]     ├── Introduction
        │   Brief introduction to the topic.
[x]     │   └── Background
        │       Context or history relevant to the topic.
[x]     │       └── Importance
        │           Why this topic matters in the current scenario.
[x]     │           └── Objective
        │               The primary goal of this document.
[x]     └── Conclusion
            Summarizing the findings and implications."""

        opt = PromptBlueprint.parse(CORPUS3, bp_text)

        print(opt)
        assert (
            opt.generate_preview_tree(preview_line_count=0, hide_comment=True)
            == BLUEPRINT_3_PARTIAL_1_PRUNED
        )


# set disable_prune  ###########################################################
# TODO TODO disable prune not working
