"""
prompt-bp-parse_basic_test.py

Unit Tests (using pytest) for: PromptBlueprint.parse()
"""

import pytest


from kaye.prompt.blueprint.prompt_blueprint import PromptBlueprint

from tests.prompt.bp import (
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


class TestDisplayName:  ########################################################

    def test_dft(_, corpus_testee1):
        bp_text = BLUEPRINT_1_FULL

        opt = PromptBlueprint.parse(bp_text, corpus_override=corpus_testee1)

        print(opt)
        assert opt.display_name == ""

    def test1(_, corpus_testee1):
        bp_text = BLUEPRINT_1_FULL
        display_name = "My Blueprint"

        opt = PromptBlueprint.parse(
            bp_text,
            display_name=display_name,
            corpus_override=corpus_testee1,
        )

        print(opt)
        assert opt.display_name == display_name

    def test2(_, corpus_testee1):
        bp_text = BLUEPRINT_1_PARTIAL_1
        display_name = "My Blueprint"

        opt = PromptBlueprint.parse(
            bp_text,
            display_name=display_name,
            corpus_override=corpus_testee1,
        )

        print(opt)
        assert opt.display_name == display_name

    def test3(_, corpus_testee3):
        bp_text = BLUEPRINT_3_EMPTY
        display_name = "My Blueprint"

        opt = PromptBlueprint.parse(
            bp_text,
            display_name=display_name,
            corpus_override=corpus_testee3,
        )

        print(opt)
        assert opt.display_name == display_name


# err handling  ################################################################
class TestErr:

    def test_malformed(_, corpus_testee1):
        bp_text = """    ○
[ ] └── Project Title
[x]     ├── Description
[x]         ├── Installation
[x]     └── License"""

        with pytest.raises(ValueError) as exec_info:
            PromptBlueprint.parse(bp_text, corpus_override=corpus_testee1)

        opt = exec_info.value.args[0]
        print(opt)

        assert (
            opt
            == """missing node heading 'Installation' in corpus that corresponds to this line:
[x]         ├── Installation"""
        )

    def test_missing_node(_, corpus_testee1):
        bp_text = """    ○
[x] └── Project Title
[x]     ├── Description
[x]     ├── Node Nonexistent In Prompt
[x]     ├── Installation
[x]     └── License"""

        with pytest.raises(ValueError) as exec_info:
            PromptBlueprint.parse(bp_text, corpus_override=corpus_testee1)

        opt = exec_info.value.args[0]
        print(opt)
        assert (
            opt
            == """missing node heading 'Node Nonexistent In Prompt' in corpus that corresponds to this line:
[x]     ├── Node Nonexistent In Prompt"""
        )


# default behavior  ############################################################
class TestDft1:  # use PROMPT1  ================================================

    def test_full(_, corpus_testee1):
        bp_text = BLUEPRINT_1_FULL

        opt = PromptBlueprint.parse(bp_text, corpus_override=corpus_testee1)

        print(repr(opt))
        assert isinstance(opt, PromptBlueprint)
        assert len(opt) == 4
        assert opt.corpus == corpus_testee1
        assert opt.display_name == ""
        assert (
            opt.generate_blueprint(content_preview_lines=0, show_comment=False)
            == bp_text
        )

    def test_part1(_, corpus_testee1):
        bp_text = BLUEPRINT_1_PARTIAL_1

        opt = PromptBlueprint.parse(bp_text, corpus_override=corpus_testee1)

        print(repr(opt))
        assert len(opt) == 4
        assert (
            opt.generate_blueprint(content_preview_lines=0, show_comment=False)
            == bp_text
        )

    def test_part2(_, corpus_testee1):
        bp_text = BLUEPRINT_1_PARTIAL_2

        bp = PromptBlueprint.parse(bp_text, corpus_override=corpus_testee1)

        opt = bp.generate_blueprint(content_preview_lines=0, show_comment=False)
        print(opt)

        assert len(bp) == 3
        assert opt == BLUEPRINT_1_PARTIAL_2_PRUNED

    def test_empty(_, corpus_testee1):
        bp_text = BLUEPRINT_1_EMPTY

        opt = PromptBlueprint.parse(bp_text, corpus_override=corpus_testee1)

        print(repr(opt))
        assert len(opt) == 0
        assert (
            opt.generate_blueprint(content_preview_lines=0, show_comment=False)
            == BLUEPRINT_EMPTY_PRUNED
        )


class TestDft2:  # use PROMPT2  ================================================

    def test_full(_, corpus_testee2):
        bp_text = BLUEPRINT_2_FULL

        opt = PromptBlueprint.parse(bp_text, corpus_override=corpus_testee2)

        print(repr(opt))
        assert isinstance(opt, PromptBlueprint)
        assert len(opt) == 7
        assert opt.corpus == corpus_testee2
        assert opt.display_name == ""
        assert (
            opt.generate_blueprint(content_preview_lines=0, show_comment=False)
            == bp_text
        )

    def test_part1(_, corpus_testee2):
        bp_text = BLUEPRINT_2_PARTIAL_1
        bp = PromptBlueprint.parse(
            bp_text,
            corpus_override=corpus_testee2,
        )

        print(repr(bp))
        assert len(bp) == 3
        assert (
            bp.generate_blueprint(content_preview_lines=0, show_comment=False)
            == BLUEPRINT_2_PARTIAL_1_PRUNED
        )

    def test_empty(_, corpus_testee2):
        bp_text = BLUEPRINT_2_EMPTY

        opt = PromptBlueprint.parse(bp_text, corpus_override=corpus_testee2)

        print(repr(opt))
        assert len(opt) == 0
        assert (
            opt.generate_blueprint(content_preview_lines=0, show_comment=False)
            == BLUEPRINT_EMPTY_PRUNED
        )


class TestDft3:  # use PROMPT3  ================================================

    def test_full(_, corpus_testee3):
        bp_text = BLUEPRINT_3_FULL

        opt = PromptBlueprint.parse(bp_text, corpus_override=corpus_testee3)

        print(repr(opt))
        assert isinstance(opt, PromptBlueprint)
        assert len(opt) == 10
        assert opt.corpus == corpus_testee3
        assert opt.display_name == ""
        assert (
            opt.generate_blueprint(content_preview_lines=0, show_comment=False)
            == bp_text
        )

    def test_part1(_, corpus_testee3):
        bp_text = BLUEPRINT_3_PARTIAL_1

        opt = PromptBlueprint.parse(bp_text, corpus_override=corpus_testee3)

        print(repr(opt))
        assert len(opt) == 6
        assert (
            opt.generate_blueprint(content_preview_lines=0, show_comment=False)
            == BLUEPRINT_3_PARTIAL_1_PRUNED
        )

    def test_part2(_, corpus_testee3):
        bp_text = BLUEPRINT_3_PARTIAL_2
        opt = PromptBlueprint.parse(bp_text, corpus_override=corpus_testee3)

        print(repr(opt))
        assert len(opt) == 9
        assert (
            opt.generate_blueprint(content_preview_lines=0, show_comment=False)
            == BLUEPRINT_3_PARTIAL_2_PRUNED
        )

    def test_empty(_, corpus_testee3):
        bp_text = BLUEPRINT_3_EMPTY
        opt = PromptBlueprint.parse(bp_text, corpus_override=corpus_testee3)

        print(repr(opt))
        assert len(opt) == 0
        assert (
            opt.generate_blueprint(content_preview_lines=0, show_comment=False)
            == BLUEPRINT_EMPTY_PRUNED
        )


# text include content preview  ################################################
class TestContentPreview1:  # use PROMPT1  =====================================

    def test1(_, corpus_testee1):
        bp_text = BLUEPRINT_1_FULL_PREVIEW

        opt = PromptBlueprint.parse(bp_text, corpus_override=corpus_testee1)

        print(repr(opt))
        assert (
            opt.generate_blueprint(content_preview_lines=0, show_comment=False)
            == BLUEPRINT_1_FULL
        )

    def test_pa1(_, corpus_testee1):
        bp_text = BLUEPRINT_1_PARTIAL_1_PREVIEW

        opt = PromptBlueprint.parse(bp_text, corpus_override=corpus_testee1)

        print(repr(opt))
        assert (
            opt.generate_blueprint(content_preview_lines=0, show_comment=False)
            == BLUEPRINT_1_PARTIAL_1
        )

    def test_pa2(_, corpus_testee1):
        bp_text = BLUEPRINT_1_PARTIAL_2_PREVIEW

        opt = PromptBlueprint.parse(bp_text, corpus_override=corpus_testee1)

        print(repr(opt))
        assert (
            opt.generate_blueprint(content_preview_lines=0, show_comment=False)
            == BLUEPRINT_1_PARTIAL_2_PRUNED
        )


class TestContentPreview2:  # use PROMPT2  =====================================

    def test_full(_, corpus_testee2):
        bp_text = BLUEPRINT_2_PREVIEW

        opt = PromptBlueprint.parse(bp_text, corpus_override=corpus_testee2)

        print(repr(opt))
        assert (
            opt.generate_blueprint(content_preview_lines=0, show_comment=False)
            == BLUEPRINT_2_FULL
        )

    def test_pa1(_, corpus_testee2):
        bp_text = BLUEPRINT_2_PARTIAL_1_PREVIEW

        opt = PromptBlueprint.parse(bp_text, corpus_override=corpus_testee2)

        print(repr(opt))
        assert (
            opt.generate_blueprint(content_preview_lines=0, show_comment=False)
            == BLUEPRINT_2_PARTIAL_1_PRUNED
        )


class TestContentPreview3:  # use PROMPT2  =====================================

    def test_full(_, corpus_testee3):
        bp_text = BLUEPRINT_3_FULL_PREVIEW

        opt = PromptBlueprint.parse(bp_text, corpus_override=corpus_testee3)

        print(repr(opt))
        assert (
            opt.generate_blueprint(content_preview_lines=0, show_comment=False)
            == BLUEPRINT_3_FULL
        )

    def test_pa1(_, corpus_testee3):
        bp_text = BLUEPRINT_3_PARTIAL_1_PREVIEW

        opt = PromptBlueprint.parse(bp_text, corpus_override=corpus_testee3)

        print(repr(opt))
        assert (
            opt.generate_blueprint(content_preview_lines=0, show_comment=False)
            == BLUEPRINT_3_PARTIAL_1_PRUNED
        )

    def test_pa2(_, corpus_testee3):
        bp_text = BLUEPRINT_3_PARTIAL_2_PREVIEW

        opt = PromptBlueprint.parse(bp_text, corpus_override=corpus_testee3)

        print(repr(opt))
        assert (
            opt.generate_blueprint(content_preview_lines=0, show_comment=False)
            == BLUEPRINT_3_PARTIAL_2_PRUNED
        )


# bp text is pruned  ###########################################################
class TestPrunedText:

    def test1(_, corpus_testee1):
        bp_text = BLUEPRINT_1_PARTIAL_2_PRUNED

        opt = PromptBlueprint.parse(bp_text, corpus_override=corpus_testee1)

        print(repr(opt))
        assert (
            opt.generate_blueprint(content_preview_lines=0, show_comment=False)
            == bp_text
        )

    def test2(_, corpus_testee2):
        bp_text = BLUEPRINT_2_PARTIAL_1_PRUNED

        opt = PromptBlueprint.parse(bp_text, corpus_override=corpus_testee2)

        print(repr(opt))
        assert (
            opt.generate_blueprint(content_preview_lines=0, show_comment=False)
            == bp_text
        )

    def test31(_, corpus_testee3):
        bp_text = BLUEPRINT_3_PARTIAL_1_PRUNED

        opt = PromptBlueprint.parse(bp_text, corpus_override=corpus_testee3)

        print(repr(opt))
        assert (
            opt.generate_blueprint(content_preview_lines=0, show_comment=False)
            == bp_text
        )

    def test32(_, corpus_testee3):
        bp_text = BLUEPRINT_3_PARTIAL_2_PRUNED

        opt = PromptBlueprint.parse(bp_text, corpus_override=corpus_testee3)

        print(repr(opt))
        assert (
            opt.generate_blueprint(content_preview_lines=0, show_comment=False)
            == bp_text
        )

    def test_pruned_input(_, corpus_testee3):
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

        opt = PromptBlueprint.parse(bp_text, corpus_override=corpus_testee3)

        print(repr(opt))
        assert (
            opt.generate_blueprint(content_preview_lines=0, show_comment=False)
            == BLUEPRINT_3_PARTIAL_1_PRUNED
        )


# malformed  ###################################################################
class TestMalformed:

    def test1(_, corpus_testee3):
        bp_text = """    ○
[x]     └── Main Title"""

        with pytest.raises(Exception) as exec_info:
            PromptBlueprint.parse(bp_text, corpus_override=corpus_testee3)
        opt = exec_info.value.args[0]

        print(opt)
        assert opt == """malformed tree format at line:
[x]     └── Main Title"""

        ""

    def test2(_, corpus_testee3):
        bp_text = """    ○
[x] └── Main Title
[x]     ├── Introduction
[x]     │       └── Background
[x]     │           └── Importance
[x]     │               └── Objective
[ ]     ├── Methods
[ ]     │   └── Data Collection
[ ]     │       └── Tools Used
[ ]     │           └── Future Work
[x]     └── Conclusion"""

        with pytest.raises(Exception) as exec_info:
            PromptBlueprint.parse(bp_text, corpus_override=corpus_testee3)
        opt = exec_info.value.args[0]

        print(opt)
        assert opt == """malformed tree format at line:
[x]     │       └── Background"""
