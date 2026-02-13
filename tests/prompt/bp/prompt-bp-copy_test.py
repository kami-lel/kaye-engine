"""
prompt-bp-copy_test.py

Unit Tests (using pytest) for: PromptCorpusNode:

- .__copy__()
- .__deepcopy__()
"""

import copy


from kaye.gen_prompt.prompt_blueprint import PromptBlueprint


from tests.prompt.bp import BLUEPRINT_3_PARTIAL_1

# TODO unit test for dynamic node


class TestCopy:

    def test_copy1(_, corpus_testee3):
        src_bp = PromptBlueprint.parse(
            BLUEPRINT_3_PARTIAL_1, corpus_override=corpus_testee3
        )

        copied = copy.copy(src_bp)

        print(copied.generate_blueprint())

        assert copied.display_name == src_bp.display_name
        assert copied.corpus == src_bp.corpus
        # test per entries
        for k, v in copied.items():
            assert k in src_bp
            assert src_bp[k] == v

    def test_deepcopy1(_, corpus_testee3):
        src_bp = PromptBlueprint.parse(
            BLUEPRINT_3_PARTIAL_1, corpus_override=corpus_testee3
        )

        copied = copy.deepcopy(src_bp)

        print(copied.generate_blueprint())

        assert copied.display_name == src_bp.display_name
        assert copied.corpus == src_bp.corpus
        # test per entries
        for k, v in copied.items():
            assert k in src_bp
            assert src_bp[k] == v
