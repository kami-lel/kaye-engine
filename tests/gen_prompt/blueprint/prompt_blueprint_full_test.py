"""
prompt_blueprint_full_test.py

Unit Tests (using pytest) for: PromptBlueprint

- .create_full_blueprint()
- .create_empty_blueprint()
"""

from kaye.gen_prompt import PromptBlueprint, PromptCorpusNode

from tests.gen_prompt import PROMPT1, PROMPT2
from tests.gen_prompt.blueprint import (
    BLUEPRINT_1_FULL,
    BLUEPRINT_2_FULL,
    BLUEPRINT_1_FULL_EMPTY,
    BLUEPRINT_2_FULL_EMPTY,
)

CORPUS1 = PromptCorpusNode.parse(PROMPT1)
CORPUS2 = PromptCorpusNode.parse(PROMPT2)

# BUG BUG BUG need test
# test .create_full_blueprint()  ###############################################


class TestFull1:

    def test_dft(_):
        corpus = CORPUS1

        bp = PromptBlueprint.create_full_blueprint(corpus)
        opt = bp.generate_preview_tree(preview_line_count=0, hide_comment=True)

        print(opt)
        assert opt == BLUEPRINT_1_FULL
        assert bp.display_name == "full"

    def test_name(_):
        corpus = CORPUS1
        display_name = "My Full Blueprint"

        bp = PromptBlueprint.create_full_blueprint(corpus)
        opt = bp.generate_preview_tree(preview_line_count=0, hide_comment=True)

        print(opt)
        assert opt == BLUEPRINT_1_FULL
        assert bp.display_name == display_name


class TestFull2:

    def test_dft(_):
        corpus = CORPUS2

        bp = PromptBlueprint.create_full_blueprint(corpus)
        opt = bp.generate_preview_tree(preview_line_count=0, hide_comment=True)

        print(opt)
        assert opt == BLUEPRINT_2_FULL
        assert bp.display_name == "full"

    def test_name(_):
        corpus = CORPUS2
        display_name = "My Full Blueprint"

        bp = PromptBlueprint.create_full_blueprint(corpus)
        opt = bp.generate_preview_tree(preview_line_count=0, hide_comment=True)

        print(opt)
        assert opt == BLUEPRINT_2_FULL
        assert bp.display_name == display_name


# test .create_empty_blueprint()  ##############################################


class TestEmpty1:

    def test_dft(_):
        corpus = CORPUS1

        bp = PromptBlueprint.create_full_blueprint(corpus)
        opt = bp.generate_preview_tree(preview_line_count=0, hide_comment=True)

        print(opt)
        assert opt == BLUEPRINT_1_FULL_EMPTY
        assert bp.display_name == "full"

    def test_name(_):
        corpus = CORPUS1
        display_name = "My Empty Blueprint"

        bp = PromptBlueprint.create_full_blueprint(corpus)
        opt = bp.generate_preview_tree(preview_line_count=0, hide_comment=True)

        print(opt)
        assert opt == BLUEPRINT_1_FULL_EMPTY
        assert bp.display_name == display_name


class TestEmpty:

    def test_dft(_):
        corpus = CORPUS2

        bp = PromptBlueprint.create_full_blueprint(corpus)
        opt = bp.generate_preview_tree(preview_line_count=0, hide_comment=True)

        print(opt)
        assert opt == BLUEPRINT_2_FULL_EMPTY
        assert bp.display_name == "empty"

    def test_name(_):
        corpus = CORPUS2
        display_name = "My Empty Blueprint"

        bp = PromptBlueprint.create_full_blueprint(corpus)
        opt = bp.generate_preview_tree(preview_line_count=0, hide_comment=True)

        print(opt)
        assert opt == BLUEPRINT_2_FULL_EMPTY
        assert bp.display_name == display_name
