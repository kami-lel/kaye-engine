"""
prompt-bp-prune_test.py

Unit Tests (using pytest) for: PromptBlueprint.prune()
"""

from kaye.prompt import PromptBlueprint

from tests.prompt.bp import (
    BLUEPRINT_1_FULL,
    BLUEPRINT_1_PARTIAL_1,
    BLUEPRINT_1_PARTIAL_2,
    BLUEPRINT_1_PARTIAL_2_PRUNED,
    BLUEPRINT_1_EMPTY,
    BLUEPRINT_2_FULL,
    BLUEPRINT_2_PARTIAL_1_PRUNED,
    BLUEPRINT_2_EMPTY,
    BLUEPRINT_3_FULL,
    BLUEPRINT_3_PARTIAL_1,
    BLUEPRINT_3_PARTIAL_1_PRUNED,
    BLUEPRINT_3_PARTIAL_2,
    BLUEPRINT_3_PARTIAL_2_PRUNED,
    BLUEPRINT_3_EMPTY,
    BLUEPRINT_EMPTY_PRUNED,
)


class Test1:  # use PROMPT1  ###################################################

    def test1(_, corpus_testee1):
        bp_text = BLUEPRINT_1_PARTIAL_2
        old = PromptBlueprint.parse(
            bp_text, disable_prune=True, corpus_override=corpus_testee1
        )

        pruned_bp = old.prune()

        pruned_bp_text = pruned_bp.generate_blueprint(
            content_preview_lines=0, show_full_tree=False
        )
        print(pruned_bp_text)

        assert len(pruned_bp) == 3
        assert pruned_bp_text == BLUEPRINT_1_PARTIAL_2_PRUNED

    def test_no_prune1(_, corpus_testee1):
        bp_text = BLUEPRINT_1_PARTIAL_1
        old = PromptBlueprint.parse(
            bp_text, disable_prune=True, corpus_override=corpus_testee1
        )

        pruned_bp = old.prune()

        pruned_bp_text = pruned_bp.generate_blueprint(
            content_preview_lines=0, show_full_tree=False
        )
        print(pruned_bp_text)

        print(pruned_bp)
        assert len(pruned_bp) == len(old)
        assert pruned_bp_text == bp_text

    def test_full(_, corpus_testee1):
        bp_text = BLUEPRINT_1_FULL
        old = PromptBlueprint.parse(
            bp_text, disable_prune=True, corpus_override=corpus_testee1
        )

        pruned_bp = old.prune()

        pruned_bp_text = pruned_bp.generate_blueprint(
            content_preview_lines=0, show_full_tree=False
        )
        print(pruned_bp_text)

        assert len(pruned_bp) == len(old)
        assert pruned_bp_text == bp_text

    def test_empty(_, corpus_testee1):
        bp_text = BLUEPRINT_1_EMPTY
        old = PromptBlueprint.parse(
            bp_text, disable_prune=True, corpus_override=corpus_testee1
        )

        pruned_bp = old.prune()

        pruned_bp_text = pruned_bp.generate_blueprint(
            content_preview_lines=0, show_full_tree=False
        )
        print(pruned_bp_text)

        assert len(pruned_bp) == 0
        assert pruned_bp_text == BLUEPRINT_EMPTY_PRUNED


class Test2:  # use PROMPT2  ###################################################

    def test1(_, bp_testee2pa1):
        old = bp_testee2pa1

        pruned_bp = old.prune()

        print(pruned_bp)
        assert len(pruned_bp) == 3
        assert (
            pruned_bp.generate_blueprint(
                content_preview_lines=0,
                show_comment=False,
                show_full_tree=False,
            )
            == BLUEPRINT_2_PARTIAL_1_PRUNED
        )

    def test_full(_, corpus_testee2):  # no prune
        bp_text = BLUEPRINT_2_FULL
        old = PromptBlueprint.parse(
            bp_text, disable_prune=True, corpus_override=corpus_testee2
        )

        pruned_bp = old.prune()

        print(pruned_bp)
        assert len(pruned_bp) == len(old)
        assert (
            pruned_bp.generate_blueprint(
                content_preview_lines=0,
                show_comment=False,
                show_full_tree=False,
            )
            == bp_text
        )

    def test_empty(_, corpus_testee2):
        bp_text = BLUEPRINT_2_EMPTY
        old = PromptBlueprint.parse(
            bp_text, disable_prune=True, corpus_override=corpus_testee2
        )

        pruned_bp = old.prune()

        print(pruned_bp)
        assert len(pruned_bp) == 0
        assert (
            pruned_bp.generate_blueprint(
                content_preview_lines=0,
                show_comment=False,
                show_full_tree=False,
            )
            == BLUEPRINT_EMPTY_PRUNED
        )


class Test3:  # use PROMPT3  ###################################################

    def test1(_, corpus_testee3):
        bp_text = BLUEPRINT_3_PARTIAL_1
        old = PromptBlueprint.parse(
            bp_text, disable_prune=True, corpus_override=corpus_testee3
        )

        pruned_bp = old.prune()

        print(pruned_bp)
        assert len(pruned_bp) == 6
        assert (
            pruned_bp.generate_blueprint(
                content_preview_lines=0,
                show_comment=False,
                show_full_tree=False,
            )
            == BLUEPRINT_3_PARTIAL_1_PRUNED
        )

    def test2(_, corpus_testee3):
        bp_text = BLUEPRINT_3_PARTIAL_2
        old = PromptBlueprint.parse(
            bp_text, disable_prune=True, corpus_override=corpus_testee3
        )

        pruned_bp = old.prune()

        print(pruned_bp)
        assert len(pruned_bp) == 9
        assert (
            pruned_bp.generate_blueprint(
                content_preview_lines=0,
                show_comment=False,
                show_full_tree=False,
            )
            == BLUEPRINT_3_PARTIAL_2_PRUNED
        )

    def test_full(_, corpus_testee3):  # no prune
        bp_text = BLUEPRINT_3_FULL
        old = PromptBlueprint.parse(
            bp_text, disable_prune=True, corpus_override=corpus_testee3
        )

        pruned_bp = old.prune()

        print(pruned_bp)
        assert len(pruned_bp) == len(old)
        assert (
            pruned_bp.generate_blueprint(
                content_preview_lines=0,
                show_comment=False,
                show_full_tree=False,
            )
            == bp_text
        )

    def test_empty(_, corpus_testee3):
        bp_text = BLUEPRINT_3_EMPTY
        old = PromptBlueprint.parse(
            bp_text, disable_prune=True, corpus_override=corpus_testee3
        )

        pruned_bp = old.prune()

        print(pruned_bp)
        assert len(pruned_bp) == 0
        assert (
            pruned_bp.generate_blueprint(
                content_preview_lines=0,
                show_comment=False,
                show_full_tree=False,
            )
            == BLUEPRINT_EMPTY_PRUNED
        )


class TestDynamicNodes:  #######################################################

    def test_abbr(_, dynamic_bp_testee1):
        pruned = dynamic_bp_testee1.prune()

        opt = pruned.generate_blueprint(content_preview_lines=0)
        print(opt)

        assert opt == """    ○
[x] ├── Main Title
[x] │   ├── Introduction
[x] │   │   └── Background
[x] │   │       └── Importance
[x] │   │           └── Objective
[x] │   ├── Methods
[x] │   │   └── Data Collection
[x] │   │       └── Tools Used
[x] │   │           └── Future Work
[x] │   └── Conclusion
[x] ├── {Today}
[x] ├── {Abbreviations}
[x] ├── {Usable Abbreviations}
[x] └── {Languages Code}"""
