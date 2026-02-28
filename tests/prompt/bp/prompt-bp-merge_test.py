"""
prompt-bp-merge_test.py

Unit Tests (using pytest) for: PromptBlueprint

- .merge()
- .__or__()
"""

import copy

import pytest


from kaye.prompt.prompt_blueprint import PromptBlueprint

# TODO TODO write tests for merge


# .merge()  ####################################################################


class TestMergeErr:

    def test_mismatched_tree(_, bp_testee1full, bp_testee2full):
        bp = bp_testee1full
        other = bp_testee2full

        with pytest.raises(ValueError) as exec_info:
            bp.merge(other)

        opt = exec_info.value.args[0]

        print(opt)
        assert opt == "must merge blueprint of same prompt tree"


# __or__  ######################################################################


class TestOrErr:

    def test_type1(_, bp_testee1full):
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

    def test_mismatched_tree(_, bp_testee1full, bp_testee2full):
        bp = bp_testee1full
        other = bp_testee2full

        with pytest.raises(ValueError) as exec_info:
            bp | other

        opt = exec_info.value.args[0]

        print(opt)
        assert opt == "must merge blueprint of same prompt tree"
