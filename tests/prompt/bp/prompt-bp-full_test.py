"""
prompt-bp-full_test.py

Unit Tests (using pytest) for: PromptBlueprint

- .create_full_blueprint()
- .create_empty_blueprint()
"""

from kaye.prompt import PromptBlueprint

from tests.prompt.bp import (
    BLUEPRINT_1_FULL,
    BLUEPRINT_2_FULL,
    BLUEPRINT_1_EMPTY,
    BLUEPRINT_2_EMPTY,
)


# test .create_full_blueprint()  ###############################################
class TestFull1:  # ============================================================

    def test_dft(_, corpus_testee1):
        bp = PromptBlueprint.create_full_blueprint(
            corpus_override=corpus_testee1
        )
        opt = bp.generate_blueprint(content_preview_lines=0, show_comment=False)

        print(opt)
        assert opt == BLUEPRINT_1_FULL


class TestFull2:  # ============================================================

    def test_dft(_, corpus_testee2):
        bp = PromptBlueprint.create_full_blueprint(
            corpus_override=corpus_testee2
        )
        opt = bp.generate_blueprint(content_preview_lines=0, show_comment=False)

        print(opt)
        assert opt == BLUEPRINT_2_FULL


# test .create_empty_blueprint()  ##############################################
class TestEmpty1:  # ===========================================================

    def test_dft(_, corpus_testee1):
        bp = PromptBlueprint.create_empty_blueprint(
            corpus_override=corpus_testee1
        )
        opt = bp.generate_blueprint(content_preview_lines=0, show_comment=False)

        print(opt)
        assert opt == BLUEPRINT_1_EMPTY


class TestEmpty2:  # ===========================================================

    def test_dft(_, corpus_testee2):
        bp = PromptBlueprint.create_empty_blueprint(
            corpus_override=corpus_testee2
        )
        opt = bp.generate_blueprint(content_preview_lines=0, show_comment=False)

        print(opt)
        assert opt == BLUEPRINT_2_EMPTY
