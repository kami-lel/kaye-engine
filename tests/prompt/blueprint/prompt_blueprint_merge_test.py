"""
prompt_blueprint_merge_test.py

Unit Tests (using pytest) for:

- .merge()
- .__imul__()
"""

import pytest
from kaye.gen_prompt import PromptBlueprint, PromptCorpusNode

from tests.prompt import PROMPT1, PROMPT3
from tests.prompt.blueprint import (
    BLUEPRINT_1_PARTIAL_1,
    BLUEPRINT_3_PARTIAL_1,
    BLUEPRINT_3_PARTIAL_1_PREVIEW,
    BLUEPRINT_3_PARTIAL_1_PRUNED,
    BLUEPRINT_3_PARTIAL_2,
    BLUEPRINT_3_PARTIAL_2_PREVIEW,
    BLUEPRINT_3_PARTIAL_2_PRUNED,
    BLUEPRINT_3_EMPTY,
)

CORPUS1 = PromptCorpusNode.parse(PROMPT1)
CORPUS3 = PromptCorpusNode.parse(PROMPT3)
BP1_PARTIAL1 = PromptBlueprint.parse(CORPUS1, BLUEPRINT_1_PARTIAL_1)
BP3_PARTIAL1 = PromptBlueprint.parse(CORPUS3, BLUEPRINT_3_PARTIAL_1)
BP3_PARTIAL2 = PromptBlueprint.parse(CORPUS3, BLUEPRINT_3_PARTIAL_2)

# test .merge()  ###############################################################


class TestMerge1:

    left_bp = BP3_PARTIAL1
    right_bp = BP3_PARTIAL2

    # TODO TODO

    # err handling  ************************************************************
    def test_bad_type(self):
        bp = self.left_bp.copy()

        with pytest.raises(ValueError) as exec_info:
            bp.merge(BP1_PARTIAL1)

        opt = exec_info.value.args[0]
        print(opt)

        assert opt == "must merge 2 blueprints with same corpus"

    def test_bad_corpus(self):
        bp = self.left_bp.copy()

        with pytest.raises(TypeError) as exec_info:
            bp.merge(15.0)

        opt = exec_info.value.args[0]
        print(opt)

        assert opt == "must merge another PromptBlueprint, not: 15.0"


class TestMerge2:

    left_bp = BP3_PARTIAL1
    right_bp = None

    # TODO TODO


# test .__imul__()  ############################################################


class TestIMul:

    left_bp = BP3_PARTIAL1
    right_bp = BP3_PARTIAL2

    # TODO TODO

    pass
