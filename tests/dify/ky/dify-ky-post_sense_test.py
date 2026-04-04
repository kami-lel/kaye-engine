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

    def test1(_):
        pass  # TODO
