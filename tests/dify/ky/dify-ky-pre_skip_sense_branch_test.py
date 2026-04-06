"""
dify-ky-pre_skip_sense_branch_test.py

Unit Tests (using pytest) for:

``pre_skip_sense_branch`` node of Kaye Chat Dify App
"""

import pytest

from dify_studio.kaye_chat.nodes.sense import pre_skip_sense_branch
from dify_studio.kaye_chat.nodes.sense.pre_skip_sense_branch import (
    OUTPUT_SKIP_KEY,
)

# helpers  #####################################################################


def _assert_structure(opt):
    assert OUTPUT_SKIP_KEY in opt
    assert isinstance(opt[OUTPUT_SKIP_KEY], bool)


# Pytest fixtures  #############################################################


@pytest.fixture
def kwargs():
    return {"role_override": "", "difficulty_override": 0, "current_role": ""}


# Pytest unit tests  ###########################################################


class TestDft:  # ==============================================================

    def test_all_dft(_, kwargs):
        opt = pre_skip_sense_branch.main(**kwargs)

        print(opt)

        _assert_structure(opt)
        assert not opt[OUTPUT_SKIP_KEY]

    def test_dft_role(_, kwargs):
        kwargs["difficulty_override"] = 0.5

        opt = pre_skip_sense_branch.main(**kwargs)

        print(opt)

        _assert_structure(opt)
        assert not opt[OUTPUT_SKIP_KEY]


class TestStatic:  # ==============================================================

    def test_provided(_, kwargs):
        kwargs["role_override"] = "barista"
        kwargs["difficulty_override"] = 0.5

        opt = pre_skip_sense_branch.main(**kwargs)

        print(opt)

        _assert_structure(opt)
        assert opt[OUTPUT_SKIP_KEY]

    def test2(_, kwargs):
        kwargs["role_override"] = "deutschlehrer"
        kwargs["difficulty_override"] = 0.5

        opt = pre_skip_sense_branch.main(**kwargs)

        print(opt)

        _assert_structure(opt)
        assert opt[OUTPUT_SKIP_KEY]

    def test3(_, kwargs):
        kwargs["role_override"] = "tarot"
        kwargs["difficulty_override"] = 0.5

        opt = pre_skip_sense_branch.main(**kwargs)

        print(opt)

        _assert_structure(opt)
        assert opt[OUTPUT_SKIP_KEY]

    def test_dft(_, kwargs):
        kwargs["role_override"] = "barista"

        opt = pre_skip_sense_branch.main(**kwargs)

        print(opt)

        _assert_structure(opt)
        assert opt[OUTPUT_SKIP_KEY]


class TestCoder:  # ============================================================

    def test_provided(_, kwargs):
        kwargs["role_override"] = "coder"
        kwargs["difficulty_override"] = 0.5

        opt = pre_skip_sense_branch.main(**kwargs)

        print(opt)

        _assert_structure(opt)
        assert opt[OUTPUT_SKIP_KEY]

    def test_dft(_, kwargs):
        kwargs["role_override"] = "coder"
        kwargs["difficulty_override"] = 0.0

        opt = pre_skip_sense_branch.main(**kwargs)

        print(opt)

        _assert_structure(opt)
        assert not opt[OUTPUT_SKIP_KEY]


class TestOthers:  # ===========================================================

    def test_provided(_, kwargs):
        kwargs["role_override"] = "art"
        kwargs["difficulty_override"] = 0.5
        opt = pre_skip_sense_branch.main(**kwargs)

        print(opt)

        _assert_structure(opt)
        assert opt[OUTPUT_SKIP_KEY]

    def test_dft(_, kwargs):
        kwargs["role_override"] = "art"
        kwargs["difficulty_override"] = 0.0

        opt = pre_skip_sense_branch.main(**kwargs)

        print(opt)

        _assert_structure(opt)
        assert not opt[OUTPUT_SKIP_KEY]


class TestCurrent:  # ==========================================================

    def test1(_, kwargs):
        kwargs["current_role"] = "art"

        opt = pre_skip_sense_branch.main(**kwargs)

        print(opt)

        _assert_structure(opt)
        assert not opt[OUTPUT_SKIP_KEY]

    def test_override(_, kwargs):
        kwargs["current_role"] = "secretary"

        opt = pre_skip_sense_branch.main(**kwargs)

        print(opt)

        _assert_structure(opt)
        assert not opt[OUTPUT_SKIP_KEY]
