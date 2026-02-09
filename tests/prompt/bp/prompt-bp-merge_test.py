"""
prompt-bp-merge_test.py

Unit Tests (using pytest) for:

- .merge()
- .__imul__()
"""

# FIXME

import pytest
from kaye.gen_prompt import PromptBlueprint, PromptCorpusNode

from tests.prompt import PROMPT1, PROMPT3
from tests.prompt.bp import (
    BLUEPRINT_1_PARTIAL_1,
    BLUEPRINT_3_PARTIAL_1,
    BLUEPRINT_3_PARTIAL_1_PRUNED,
    BLUEPRINT_3_PARTIAL_2,
    BLUEPRINT_3_PARTIAL_2_PRUNED,
    BLUEPRINT_3_EMPTY,
    BLUEPRINT_3_FULL,
)

CORPUS1 = PromptCorpusNode.parse(PROMPT1)
CORPUS3 = PromptCorpusNode.parse(PROMPT3)
BP1_PARTIAL1 = PromptBlueprint.parse(CORPUS1, BLUEPRINT_1_PARTIAL_1)
BP3_PARTIAL1 = PromptBlueprint.parse(CORPUS3, BLUEPRINT_3_PARTIAL_1)
BP3_PARTIAL1_PRUNED = PromptBlueprint.parse(
    CORPUS3, BLUEPRINT_3_PARTIAL_1_PRUNED
)
BP3_PARTIAL2 = PromptBlueprint.parse(CORPUS3, BLUEPRINT_3_PARTIAL_2)
BP3_PARTIAL2_PRUNED = PromptBlueprint.parse(
    CORPUS3, BLUEPRINT_3_PARTIAL_2_PRUNED
)
BP3_FULL = PromptBlueprint.parse(CORPUS3, BLUEPRINT_3_FULL)
BP3_EMPTY = PromptBlueprint.parse(CORPUS3, BLUEPRINT_3_EMPTY)

# test .merge()  ###############################################################


class TestMerge1:

    left_bp = BP3_PARTIAL1
    right_bp = BP3_PARTIAL2

    def test_merge1(self):
        merged = self.left_bp.merge(self.right_bp)

        print(merged)
        assert (
            merged.generate_preview_tree(
                preview_line_count=0, hide_comment=True
            )
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
            merged.generate_preview_tree(
                preview_line_count=0, hide_comment=True
            )
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
        merged = BP3_EMPTY.merge(self.right_bp)

        print(merged)
        assert (
            merged.generate_preview_tree(
                preview_line_count=0, hide_comment=True
            )
            == BLUEPRINT_3_PARTIAL_2_PRUNED
        )

    def test_empty2(self):
        merged = self.right_bp.merge(BP3_EMPTY)

        print(merged)
        assert (
            merged.generate_preview_tree(
                preview_line_count=0, hide_comment=True
            )
            == BLUEPRINT_3_PARTIAL_2_PRUNED
        )

    def test_full1(self):
        merged = BP3_FULL.merge(self.right_bp)

        print(merged)
        assert (
            merged.generate_preview_tree(
                preview_line_count=0, hide_comment=True
            )
            == BLUEPRINT_3_FULL
        )

    def test_full2(self):
        merged = self.right_bp.merge(BP3_FULL)

        print(merged)
        assert (
            merged.generate_preview_tree(
                preview_line_count=0, hide_comment=True
            )
            == BLUEPRINT_3_FULL
        )

    # err handling  ************************************************************
    def test_bad_type(self):
        bp = self.left_bp.copy()

        with pytest.raises(ValueError) as exec_info:
            bp.merge(BP1_PARTIAL1)

        opt = exec_info.value.args[0]
        print(opt)

        assert opt == "must merge 2 bps with same corpus"

    def test_bad_corpus(self):
        bp = self.left_bp.copy()

        with pytest.raises(TypeError) as exec_info:
            bp.merge(15.0)

        opt = exec_info.value.args[0]
        print(opt)

        assert opt == "must merge another PromptBlueprint, not: 15.0"


# test .__imul__()  ############################################################
class TestIMul:

    left_bp = BP3_PARTIAL1
    right_bp = BP3_PARTIAL2

    def test_merge1(self):
        merged = self.left_bp.copy()
        merged *= self.right_bp

        print(merged)
        assert (
            merged.generate_preview_tree(
                preview_line_count=0, hide_comment=True
            )
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
