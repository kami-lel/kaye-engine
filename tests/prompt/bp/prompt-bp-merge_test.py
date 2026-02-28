"""
prompt-bp-merge_test.py

Unit Tests (using pytest) for: PromptBlueprint

- .merge()
- .__or__()
"""

import copy

import pytest


from kaye.prompt.prompt_blueprint import PromptBlueprint

from tests.prompt.bp import BLUEPRINT_1_FULL, BLUEPRINT_2_FULL, BLUEPRINT_3_FULL


class TestMerge:  # .merge()  ##################################################

    # use PROMPT 1  ============================================================

    def test1_1(_, bp_testee1pa1, bp_testee1pa2):
        bp_left = bp_testee1pa1
        bp_right = bp_testee1pa2

        opt = bp_left.merge(bp_right)
        print(opt)

        assert (
            opt.generate_blueprint(content_preview_lines=0) == BLUEPRINT_1_FULL
        )

    def test1_2(_, bp_testee1pa1, bp_testee1pa2):
        bp_left = bp_testee1pa2
        bp_right = bp_testee1pa1

        opt = bp_left.merge(bp_right)
        print(opt)

        assert (
            opt.generate_blueprint(content_preview_lines=0) == BLUEPRINT_1_FULL
        )

    # use PROMPT 2  ============================================================

    def test2_1(_, bp_testee2pa1, bp_testee2pa2):
        bp_left = bp_testee2pa1
        bp_right = bp_testee2pa2

        opt = bp_left.merge(bp_right)
        print(opt)

        assert (
            opt.generate_blueprint(content_preview_lines=0) == BLUEPRINT_2_FULL
        )

    def test2_2(_, bp_testee2pa1, bp_testee2pa2):
        bp_left = bp_testee2pa2
        bp_right = bp_testee2pa1

        opt = bp_left.merge(bp_right)
        print(opt)

        assert (
            opt.generate_blueprint(content_preview_lines=0) == BLUEPRINT_2_FULL
        )

    # use PROMPT 3  ============================================================

    def test3_1(_, bp_testee3pa1, bp_testee3pa2):
        bp_left = bp_testee3pa1
        bp_right = bp_testee3pa2

        opt = bp_left.merge(bp_right)
        print(opt)

        assert (
            opt.generate_blueprint(content_preview_lines=0) == BLUEPRINT_3_FULL
        )

    def test3_2(_, bp_testee3pa1, bp_testee3pa2):
        bp_left = bp_testee3pa2
        bp_right = bp_testee3pa1

        opt = bp_left.merge(bp_right)
        print(opt)

        assert (
            opt.generate_blueprint(content_preview_lines=0) == BLUEPRINT_3_FULL
        )

    # err handling =============================================================

    def test_err_mismatched_tree(_, bp_testee1full, bp_testee2full):
        bp = bp_testee1full
        other = bp_testee2full

        with pytest.raises(ValueError) as exec_info:
            bp.merge(other)

        opt = exec_info.value.args[0]

        print(opt)
        assert opt == "must merge blueprint of same prompt tree"


class TestOrErr:  # __or__  ####################################################

    # TODO write tests for merge

    # err handling =============================================================

    def test_err_type1(_, bp_testee1full):
        bp = bp_testee1full
        other = 123

        with pytest.raises(TypeError) as exec_info:
            bp | other

        opt = exec_info.value.args[0]

        print(opt)
        assert (
            opt
            == "unsupported operand type(s) for |: 'PromptBlueprint' and 'int'"
        )

    def test_err_mismatched(_, bp_testee1full, bp_testee2full):
        bp = bp_testee1full
        other = bp_testee2full

        with pytest.raises(ValueError) as exec_info:
            bp | other

        opt = exec_info.value.args[0]

        print(opt)
        assert opt == "must merge blueprint of same prompt tree"
