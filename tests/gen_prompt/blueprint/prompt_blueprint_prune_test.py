"""
prompt_blueprint_prune_test.py

Unit Tests (using pytest) for: PromptBlueprint.prune()
"""

from kaye.gen_prompt import PromptBlueprint, PromptCorpusNode
from tests.gen_prompt import PROMPT1, PROMPT2, PROMPT3
from tests.gen_prompt.blueprint import (
    BLUEPRINT_1_FULL,
    BLUEPRINT_1_FULL_PARTIAL_1,
    BLUEPRINT_1_FULL_PARTIAL_2,
    BLUEPRINT_1_FULL_EMPTY,
    BLUEPRINT_2_FULL,
    BLUEPRINT_2_FULL_PARTIAL_1,
    BLUEPRINT_2_FULL_EMPTY,
    BLUEPRINT_3_FULL,
    BLUEPRINT_3_FULL_PARTIAL_1,
    BLUEPRINT_3_FULL_PARTIAL_2,
    BLUEPRINT_3_FULL_EMPTY,
)


class Test1:  # use PROMPT1  ###################################################

    corpus = PromptCorpusNode.parse(PROMPT1)

    def test1(self):
        bp_text = BLUEPRINT_1_FULL_PARTIAL_2
        old = PromptBlueprint.parse(self.corpus, bp_text, disable_prune=True)

        opt = old.prune()

        print(opt)

        assert len(opt) == 3
        assert (
            opt.generate_preview_tree(preview_line_count=0, hide_comment=True)
            == """    ○
[x] └── Project Title
[x]     ├── Installation
[x]     └── License"""
        )

    def test_no_prune1(self):
        bp_text = BLUEPRINT_1_FULL_PARTIAL_1
        old = PromptBlueprint.parse(self.corpus, bp_text, disable_prune=True)

        opt = old.prune()

        print(opt)
        assert len(opt) == len(old)
        assert (
            opt.generate_preview_tree(preview_line_count=0, hide_comment=True)
            == bp_text
        )

    def test_full(self):  # no prune
        bp_text = BLUEPRINT_1_FULL
        old = PromptBlueprint.parse(self.corpus, bp_text, disable_prune=True)

        opt = old.prune()

        print(opt)
        assert len(opt) == len(old)
        assert (
            opt.generate_preview_tree(preview_line_count=0, hide_comment=True)
            == bp_text
        )

    def test_empty(self):
        bp_text = BLUEPRINT_1_FULL_EMPTY
        old = PromptBlueprint.parse(self.corpus, bp_text, disable_prune=True)

        opt = old.prune()

        print(opt)
        assert len(opt) == 0
        assert (
            opt.generate_preview_tree(preview_line_count=0, hide_comment=True)
            == """    ○"""
        )


class Test2:  # use PROMPT1  ###################################################

    corpus = PromptCorpusNode.parse(PROMPT2)

    def test1(self):
        bp_text = BLUEPRINT_2_FULL_PARTIAL_1
        old = PromptBlueprint.parse(self.corpus, bp_text, disable_prune=True)

        opt = old.prune()

        print(opt)
        assert len(opt) == 3
        assert (
            opt.generate_preview_tree(preview_line_count=0, hide_comment=True)
            == """    ○
[x] └── Project Title
[x]     ├── Installation
[x]     └── Contributing"""
        )

    def test_full(self):  # no prune
        bp_text = BLUEPRINT_2_FULL
        old = PromptBlueprint.parse(self.corpus, bp_text, disable_prune=True)

        opt = old.prune()

        print(opt)
        assert len(opt) == len(old)
        assert (
            opt.generate_preview_tree(preview_line_count=0, hide_comment=True)
            == bp_text
        )

    def test_empty(self):
        bp_text = BLUEPRINT_2_FULL_EMPTY
        old = PromptBlueprint.parse(self.corpus, bp_text, disable_prune=True)

        opt = old.prune()

        print(opt)
        assert len(opt) == 0
        assert (
            opt.generate_preview_tree(preview_line_count=0, hide_comment=True)
            == """    ○"""
        )


class Test3:  # use PROMPT1  ###################################################

    corpus = PromptCorpusNode.parse(PROMPT3)

    def test1(self):
        bp_text = BLUEPRINT_3_FULL_PARTIAL_1
        old = PromptBlueprint.parse(self.corpus, bp_text, disable_prune=True)

        opt = old.prune()

        print(opt)
        assert len(opt) == 6
        assert (
            opt.generate_preview_tree(preview_line_count=0, hide_comment=True)
            == """    ○
[x] └── Main Title
[x]     ├── Introduction
[x]     │   └── Background
[x]     │       └── Importance
[x]     │           └── Objective
[x]     └── Conclusion"""
        )

    def test2(self):
        bp_text = BLUEPRINT_3_FULL_PARTIAL_2
        old = PromptBlueprint.parse(self.corpus, bp_text, disable_prune=True)

        opt = old.prune()

        print(opt)
        assert len(opt) == 9
        assert (
            opt.generate_preview_tree(preview_line_count=0, hide_comment=True)
            == """    ○
[x] └── Main Title
[ ]     ├── Introduction
[x]     │   └── Background
[ ]     │       └── Importance
[x]     │           └── Objective
[ ]     └── Methods
[x]         └── Data Collection
[ ]             └── Tools Used
[x]                 └── Future Work"""
        )

    def test_full(self):  # no prune
        bp_text = BLUEPRINT_3_FULL
        old = PromptBlueprint.parse(self.corpus, bp_text, disable_prune=True)

        opt = old.prune()

        print(opt)
        assert len(opt) == len(old)
        assert (
            opt.generate_preview_tree(preview_line_count=0, hide_comment=True)
            == bp_text
        )

    def test_empty(self):
        bp_text = BLUEPRINT_3_FULL_EMPTY
        old = PromptBlueprint.parse(self.corpus, bp_text, disable_prune=True)

        opt = old.prune()

        print(opt)
        assert len(opt) == 0
        assert (
            opt.generate_preview_tree(preview_line_count=0, hide_comment=True)
            == """    ○"""
        )
