"""
prompt-bp-merge_test.py

Unit Tests (using pytest) for:

- .merge()
- .__imul__()
"""

# Fixme

import pytest
from kaye.gen_prompt import PromptBlueprint, PromptCorpusNode

from tests.prompt.bp import (
    BLUEPRINT_1_PARTIAL_1,
    BLUEPRINT_3_PARTIAL_1,
    BLUEPRINT_3_PARTIAL_1_PRUNED,
    BLUEPRINT_3_PARTIAL_2,
    BLUEPRINT_3_PARTIAL_2_PRUNED,
    BLUEPRINT_3_EMPTY,
    BLUEPRINT_3_FULL,
)

BP1_PARTIAL1 = None  # PromptBlueprint.parse(BLUEPRINT_1_PARTIAL_1)
BP3_PARTIAL1 = None  # PromptBlueprint.parse(BLUEPRINT_3_PARTIAL_1)
BP3_PARTIAL1_PRUNED = (
    None  # PromptBlueprint.parse(BLUEPRINT_3_PARTIAL_1_PRUNED)
)
BP3_PARTIAL2 = None  # PromptBlueprint.parse(BLUEPRINT_3_PARTIAL_2)
BP3_PARTIAL2_PRUNED = (
    None  # PromptBlueprint.parse(BLUEPRINT_3_PARTIAL_2_PRUNED)
)
BP3_FULL = None  # PromptBlueprint.parse(BLUEPRINT_3_FULL)
BP3_EMPTY = None  # PromptBlueprint.parse(BLUEPRINT_3_EMPTY)


# fixtures  ####################################################################


@pytest.fixture()
def corpus3_blueprint_partial1(test_corpus3):
    return PromptBlueprint.parse(
        BLUEPRINT_3_PARTIAL_1, prompt_corpus_override=test_corpus3
    )


@pytest.fixture()
def corpus3_blueprint_partial2(test_corpus3):
    return PromptBlueprint.parse(
        BLUEPRINT_3_PARTIAL_2, prompt_corpus_override=test_corpus3
    )


class XTestMerge:  # test .merge()  #############################################

    def test_merge1(_, corpus3_blueprint_partial1, corpus3_blueprint_partial2):
        merged = corpus3_blueprint_partial1.merge(corpus3_blueprint_partial2)

        print(merged)
        assert (
            merged.generate_blueprint(preview_line_count=0, hide_comment=True)
            == """    ○
[x] └── Main Title
[x]     ├── Introduction
[x]     │   └── Background
[x]     │       └── Importance
[x]     │           └── Objective
[ ]     ├── Methods
[x]     │   └── Data Collection
[ ]     │       └── Tools Used
[x]     │           └── Future Work
[x]     └── Conclusion"""
        )

    def test_merge2(self):
        merged = BP3_PARTIAL1_PRUNED.merge(BP3_PARTIAL2_PRUNED)

        print(merged)
        assert (
            merged.generate_blueprint(preview_line_count=0, hide_comment=True)
            == """    ○
[x] └── Main Title
[x]     ├── Introduction
[x]     │   └── Background
[x]     │       └── Importance
[x]     │           └── Objective
[ ]     ├── Methods
[x]     │   └── Data Collection
[ ]     │       └── Tools Used
[x]     │           └── Future Work
[x]     └── Conclusion"""
        )

    def test_empty1(self):
        merged = BP3_EMPTY.merge(corpus3_blueprint_partial2)

        print(merged)
        assert (
            merged.generate_blueprint(preview_line_count=0, hide_comment=True)
            == BLUEPRINT_3_PARTIAL_2_PRUNED
        )

    def test_empty2(self):
        merged = corpus3_blueprint_partial2.merge(BP3_EMPTY)

        print(merged)
        assert (
            merged.generate_blueprint(preview_line_count=0, hide_comment=True)
            == BLUEPRINT_3_PARTIAL_2_PRUNED
        )

    def test_full1(self):
        merged = BP3_FULL.merge(corpus3_blueprint_partial2)

        print(merged)
        assert (
            merged.generate_blueprint(preview_line_count=0, hide_comment=True)
            == BLUEPRINT_3_FULL
        )

    def test_full2(self):
        merged = corpus3_blueprint_partial2.merge(BP3_FULL)

        print(merged)
        assert (
            merged.generate_blueprint(preview_line_count=0, hide_comment=True)
            == BLUEPRINT_3_FULL
        )

    # err handling  ************************************************************
    def test_bad_type(self):
        bp = corpus3_blueprint_partial1.copy()

        with pytest.raises(ValueError) as exec_info:
            bp.merge(BP1_PARTIAL1)

        opt = exec_info.value.args[0]
        print(opt)

        assert opt == "must merge 2 bps with same corpus"

    def test_bad_corpus(self):
        bp = corpus3_blueprint_partial1.copy()

        with pytest.raises(TypeError) as exec_info:
            bp.merge(15.0)

        opt = exec_info.value.args[0]
        print(opt)

        assert opt == "must merge another PromptBlueprint, not: 15.0"


class XTestIMul:  # test .__imul__()  ###########################################

    left_bp = BP3_PARTIAL1
    right_bp = BP3_PARTIAL2

    def test_merge1(self):
        merged = self.left_bp.copy()
        merged *= self.right_bp

        print(merged)
        assert (
            merged.generate_blueprint(preview_line_count=0, hide_comment=True)
            == """    ○
[x] └── Main Title
[x]     ├── Introduction
[x]     │   └── Background
[x]     │       └── Importance
[x]     │           └── Objective
[ ]     ├── Methods
[x]     │   └── Data Collection
[ ]     │       └── Tools Used
[x]     │           └── Future Work
[x]     └── Conclusion"""
        )

    # err handling  ************************************************************
    def test_bad_type(self):
        bp = self.left_bp.copy()

        with pytest.raises(ValueError) as exec_info:
            bp *= BP1_PARTIAL1

        opt = exec_info.value.args[0]
        print(opt)

        assert opt == "must merge 2 bps with same corpus"

    def test_bad_corpus(self):
        bp = self.left_bp.copy()

        with pytest.raises(TypeError) as exec_info:
            bp *= 15.0

        opt = exec_info.value.args[0]
        print(opt)

        assert opt == "must merge another PromptBlueprint, not: 15.0"
