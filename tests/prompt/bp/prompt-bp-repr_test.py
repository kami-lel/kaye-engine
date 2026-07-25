"""
prompt-bp-repr_test.py

Unit Tests (using pytest) for:

- __repr__()
"""

from kaye_engine.prompt.blueprint.prompt_blueprint import PromptBlueprint

from tests.prompt.bp import (
    BLUEPRINT_1_FULL,
    BLUEPRINT_1_FULL_PREVIEW,
    BLUEPRINT_2_FULL,
    BLUEPRINT_2_PREVIEW,
    BLUEPRINT_3_FULL,
    BLUEPRINT_3_FULL_PREVIEW,
)


class TestRepr:  ###############################################################

    def test1(_, corpus_testee1):
        corpus = corpus_testee1
        bp_text = BLUEPRINT_1_FULL

        bp = PromptBlueprint.parse(
            bp_text, disable_prune=True, corpus_override=corpus
        )
        opt = repr(bp)

        print(opt)

        assert opt == BLUEPRINT_1_FULL_PREVIEW

    def test2(_, corpus_testee2):
        corpus = corpus_testee2
        bp_text = BLUEPRINT_2_FULL

        bp = PromptBlueprint.parse(
            bp_text, disable_prune=True, corpus_override=corpus
        )
        opt = repr(bp)

        print(opt)

        assert opt == BLUEPRINT_2_PREVIEW

    def test3(_, corpus_testee3):
        corpus = corpus_testee3
        bp_text = BLUEPRINT_3_FULL

        bp = PromptBlueprint.parse(
            bp_text, disable_prune=True, corpus_override=corpus
        )
        opt = repr(bp)

        print(opt)

        assert opt == BLUEPRINT_3_FULL_PREVIEW
