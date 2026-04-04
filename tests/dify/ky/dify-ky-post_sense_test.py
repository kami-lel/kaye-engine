"""
dify-ky-post_sense_test.py

Unit Tests (using pytest) for:

post_sense node of Kaye Chat Dify App
"""

import pytest


from dify_studio.kaye_chat.nodes.sense import post_sense
from dify_studio.kaye_chat.nodes.sense.post_sense import (
    OUTPUT_ROLE_KEY,
    OUTPUT_DIFF_KEY,
    OUTPUT_PLS_KEY,
)


# helpers  #####################################################################
def _assert_structure(opt):
    assert OUTPUT_ROLE_KEY in opt
    assert OUTPUT_DIFF_KEY in opt
    assert OUTPUT_PLS_KEY in opt


# Pytest fixtures  #############################################################
@pytest.fixture
def kwargs_default():
    return {
        "sensed_role": "",
        "sensed_difficulty": 0,
        "sensed_pls": "",
        "current_role": "",
        "difficulty_override": 0,
        "current_pls": "",
    }


# Pytest unit tests  ###########################################################


class TestRole:  # =============================================================

    def test1(_, kwargs_default):
        kwargs_default["sensed_role"] = "tarot"
        kwargs_default["current_role"] = "barista"

        opt = post_sense.main(**kwargs_default)

        _assert_structure(opt)

        assert opt[OUTPUT_ROLE_KEY] == "barista"

    def test2(_, kwargs_default):
        kwargs_default["sensed_role"] = "tarot"

        opt = post_sense.main(**kwargs_default)

        _assert_structure(opt)

        assert opt[OUTPUT_ROLE_KEY] == "tarot"

    def test3(_, kwargs_default):
        opt = post_sense.main(**kwargs_default)

        _assert_structure(opt)

        assert opt[OUTPUT_ROLE_KEY] == "chat"


class TestDiff:  # =============================================================

    def test1(_, kwargs_default):
        kwargs_default["difficulty_override"] = 0.3

        opt = post_sense.main(**kwargs_default)

        _assert_structure(opt)

        assert opt[OUTPUT_DIFF_KEY] == 0.3

    def test2(_, kwargs_default):
        kwargs_default["sensed_difficulty"] = 0.6

        opt = post_sense.main(**kwargs_default)

        _assert_structure(opt)

        assert opt[OUTPUT_DIFF_KEY] == 0.6

    def test3(_, kwargs_default):
        kwargs_default["difficulty_override"] = 0.3
        kwargs_default["sensed_difficulty"] = 0.6

        opt = post_sense.main(**kwargs_default)

        _assert_structure(opt)

        assert opt[OUTPUT_DIFF_KEY] == 0.3


class TestPLs:  # ==============================================================

    def test_empty(_, kwargs_default):
        opt = post_sense.main(**kwargs_default)

        _assert_structure(opt)

        assert opt[OUTPUT_PLS_KEY] == ""

    # only sensed  *************************************************************

    def test_only_sensed1(_, kwargs_default):
        pls = "cpp"
        kwargs_default["sensed_pls"] = pls

        opt = post_sense.main(**kwargs_default)

        _assert_structure(opt)
        assert opt[OUTPUT_PLS_KEY] == pls

    def test_only_sensed2(_, kwargs_default):
        kwargs_default["sensed_pls"] = "cpp,py"

        opt = post_sense.main(**kwargs_default)

        _assert_structure(opt)
        as_set = set(opt[OUTPUT_PLS_KEY].split(","))
        assert as_set == set(["cpp", "py"])

    def test_only_sensed3(_, kwargs_default):
        kwargs_default["sensed_pls"] = "ts,cpp,py"

        opt = post_sense.main(**kwargs_default)

        _assert_structure(opt)
        as_set = set(opt[OUTPUT_PLS_KEY].split(","))
        assert as_set == set(["cpp", "ts", "py"])

    # only current  ************************************************************

    def test_only_current1(_, kwargs_default):
        pls = "cpp"
        kwargs_default["current_pls"] = pls

        opt = post_sense.main(**kwargs_default)

        _assert_structure(opt)
        assert opt[OUTPUT_PLS_KEY] == pls

    def test_only_current2(_, kwargs_default):
        kwargs_default["current_pls"] = "cpp,py"

        opt = post_sense.main(**kwargs_default)

        _assert_structure(opt)
        as_set = set(opt[OUTPUT_PLS_KEY].split(","))
        assert as_set == set(["cpp", "py"])

    def test_only_current3(_, kwargs_default):
        kwargs_default["current_pls"] = "ts,cpp,py"

        opt = post_sense.main(**kwargs_default)

        _assert_structure(opt)
        as_set = set(opt[OUTPUT_PLS_KEY].split(","))
        assert as_set == set(["cpp", "ts", "py"])

    # combine  *****************************************************************

    def test_combined1(_, kwargs_default):
        kwargs_default["sensed_pls"] = "ts,cpp,py"
        kwargs_default["current_pls"] = "ts,cpp,py"

        opt = post_sense.main(**kwargs_default)

        _assert_structure(opt)
        as_set = set(opt[OUTPUT_PLS_KEY].split(","))
        assert as_set == set(["cpp", "ts", "py"])

    def test_combined2(_, kwargs_default):
        kwargs_default["sensed_pls"] = "ts"
        kwargs_default["current_pls"] = "cpp,py"

        opt = post_sense.main(**kwargs_default)

        _assert_structure(opt)
        as_set = set(opt[OUTPUT_PLS_KEY].split(","))
        assert as_set == set(["cpp", "ts", "py"])

    def test_combined3(_, kwargs_default):
        kwargs_default["sensed_pls"] = "ts,c,rust"
        kwargs_default["current_pls"] = "cpp,py"

        opt = post_sense.main(**kwargs_default)

        _assert_structure(opt)
        as_set = set(opt[OUTPUT_PLS_KEY].split(","))
        assert as_set == set(["cpp", "ts", "py", "c", "rust"])
