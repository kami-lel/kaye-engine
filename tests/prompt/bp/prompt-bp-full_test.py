"""
prompt-bp-full_test.py

Unit Tests (using pytest) for: PromptBlueprint

- .create_full_bp()
- .create_empty_bp()
"""

# FIXME

from kaye.gen_prompt import PromptBlueprint, PromptCorpusNode

from tests.prompt.bp import (
    BLUEPRINT_1_FULL,
    BLUEPRINT_2_FULL,
    BLUEPRINT_1_EMPTY,
    BLUEPRINT_2_EMPTY,
)

# test .create_full_bp()  ###############################################


class XTestFull1:

    def test_dft(_):
        corpus = CORPUS1

        bp = PromptBlueprint.create_full_bp(corpus)
        opt = bp.generate_preview_tree(preview_line_count=0, hide_comment=True)

        print(opt)
        assert opt == BLUEPRINT_1_FULL
        assert bp.display_name == "full"

    def test_name(_):
        corpus = CORPUS1
        display_name = "My Full Blueprint"

        bp = PromptBlueprint.create_full_bp(corpus, display_name=display_name)
        opt = bp.generate_preview_tree(preview_line_count=0, hide_comment=True)

        print(opt)
        assert opt == BLUEPRINT_1_FULL
        assert bp.display_name == display_name


class XTestFull2:

    def test_dft(_):
        corpus = CORPUS2

        bp = PromptBlueprint.create_full_bp(corpus)
        opt = bp.generate_preview_tree(preview_line_count=0, hide_comment=True)

        print(opt)
        assert opt == BLUEPRINT_2_FULL
        assert bp.display_name == "full"

    def test_name(_):
        corpus = CORPUS2
        display_name = "My Full Blueprint"

        bp = PromptBlueprint.create_full_bp(corpus, display_name=display_name)
        opt = bp.generate_preview_tree(preview_line_count=0, hide_comment=True)

        print(opt)
        assert opt == BLUEPRINT_2_FULL
        assert bp.display_name == display_name


# test .create_empty_bp()  ##############################################
class XTestEmpty1:

    def test_dft(_):
        corpus = CORPUS1

        bp = PromptBlueprint.create_empty_bp(corpus)
        opt = bp.generate_preview_tree(preview_line_count=0, hide_comment=True)

        print(opt)
        assert opt == BLUEPRINT_1_EMPTY
        assert bp.display_name == "empty"

    def test_name(_):
        corpus = CORPUS1
        display_name = "My Empty Blueprint"

        bp = PromptBlueprint.create_empty_bp(corpus, display_name=display_name)
        opt = bp.generate_preview_tree(preview_line_count=0, hide_comment=True)

        print(opt)
        assert opt == BLUEPRINT_1_EMPTY
        assert bp.display_name == display_name


class XTestEmpty:

    def test_dft(_):
        corpus = CORPUS2

        bp = PromptBlueprint.create_empty_bp(corpus)
        opt = bp.generate_preview_tree(preview_line_count=0, hide_comment=True)

        print(opt)
        assert opt == BLUEPRINT_2_EMPTY
        assert bp.display_name == "empty"

    def test_name(_):
        corpus = CORPUS2
        display_name = "My Empty Blueprint"

        bp = PromptBlueprint.create_empty_bp(corpus, display_name=display_name)
        opt = bp.generate_preview_tree(preview_line_count=0, hide_comment=True)

        print(opt)
        assert opt == BLUEPRINT_2_EMPTY
        assert bp.display_name == display_name
