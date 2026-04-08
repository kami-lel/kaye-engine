"""
api-ky-sense-coder_test.py

Unit Tests (using pytest) for:

/kaye/dify-app/ky/sense to sense for coder
"""

import pytest


from tests.api.ky.sense import (
    _assert_sense_title1,
    _assert_sense_title2,
    _assert_zero_diff1,
    _assert_zero_diff2,
    _assert_empty_role1,
    _assert_empty_role2,
)

# helpers  #####################################################################


def _assert_pl_instruction_title(opt):
    assert "### programming_languages" in opt


def _assert_pl_instruction1(opt):
    assert "Return a string containing the abbreviations" in opt


def _assert_pl_instruction2(opt):
    assert 'For example, `"py,cpp,ue"`.' in opt


# PLCs  ------------------------------------------------------------------------


def _assert_plc_title(opt):
    assert "# {Programming Languages Code}" in opt


def _assert_plc1(opt):
    assert "-`bash`:Bash" in opt


def _assert_plc2(opt):
    assert "-`csharp`:C Sharp" in opt


def _assert_plc3(opt):
    assert "-`c`:C language" in opt


def _assert_plc4(opt):
    assert "-`cpp`:C++" in opt


def _assert_plc5(opt):
    assert "-`html`:HTML" in opt


def _assert_plc6(opt):
    assert "-`py`:Python" in opt


def _assert_plc7(opt):
    assert "-`qt`:Qt framework" in opt


def _assert_plc8(opt):
    assert "-`u3d`:Unity Engine code" in opt


def _assert_plc9(opt):
    assert "-`ue`:Unreal Engine code" in opt


# Pytest fixtures  #############################################################
@pytest.fixture(scope="class")
def opt_diff_override(flask_test_client, sense_endpoint):
    request_body = {"pre_sense_role": "coder", "difficulty_override": 15}

    response = flask_test_client.post(sense_endpoint, json=request_body)
    return response.get_data().decode("utf-8")


@pytest.fixture(scope="class")
def opt_no_diff(flask_test_client, sense_endpoint):
    request_body = {"pre_sense_role": "coder", "difficulty_override": 0}

    response = flask_test_client.post(sense_endpoint, json=request_body)
    return response.get_data().decode("utf-8")


# Pytest unit tests  ###########################################################


class TestDiffOverride:  # =====================================================

    # title  -------------------------------------------------------------------

    def test_sense_title1(_, opt_diff_override):
        opt = opt_diff_override
        print(opt)
        _assert_sense_title1(opt)

    def test_sense_title2(_, opt_diff_override):
        opt = opt_diff_override
        print(opt)
        _assert_sense_title2(opt)

    # pl -----------------------------------------------------------------------

    def test_pl_instruction_title(_, opt_diff_override):
        opt = opt_diff_override
        print(opt)
        _assert_pl_instruction_title(opt)

    def test_pl_instruction1(_, opt_diff_override):
        opt = opt_diff_override
        print(opt)
        _assert_pl_instruction1(opt)

    def test_pl_instruction2(_, opt_diff_override):
        opt = opt_diff_override
        print(opt)
        _assert_pl_instruction2(opt)

    # plc  ---------------------------------------------------------------------

    def test_plc_title(_, opt_diff_override):
        opt = opt_diff_override
        print(opt)
        _assert_plc_title(opt)

    def test_pl1(_, opt_diff_override):
        opt = opt_diff_override
        print(opt)
        _assert_plc1(opt)

    def test_pl2(_, opt_diff_override):
        opt = opt_diff_override
        print(opt)
        _assert_plc2(opt)

    def test_pl3(_, opt_diff_override):
        opt = opt_diff_override
        print(opt)
        _assert_plc3(opt)

    def test_pl4(_, opt_diff_override):
        opt = opt_diff_override
        print(opt)
        _assert_plc4(opt)

    def test_pl5(_, opt_diff_override):
        opt = opt_diff_override
        print(opt)
        _assert_plc5(opt)

    def test_pl6(_, opt_diff_override):
        opt = opt_diff_override
        print(opt)
        _assert_plc6(opt)

    def test_pl7(_, opt_diff_override):
        opt = opt_diff_override
        print(opt)
        _assert_plc7(opt)

    def test_pl8(_, opt_diff_override):
        opt = opt_diff_override
        print(opt)
        _assert_plc8(opt)

    def test_pl9(_, opt_diff_override):
        opt = opt_diff_override
        print(opt)
        _assert_plc9(opt)

    # zero diff  ---------------------------------------------------------------

    def test_zero_diff1(_, opt_diff_override):
        opt = opt_diff_override
        print(opt)
        _assert_zero_diff1(opt)

    def test_zero_diff2(_, opt_diff_override):
        opt = opt_diff_override
        print(opt)
        _assert_zero_diff2(opt)

    # empty role  --------------------------------------------------------------

    def test_empty_role1(_, opt_diff_override):
        opt = opt_diff_override
        print(opt)
        _assert_empty_role1(opt)

    def test_empty_role2(_, opt_diff_override):
        opt = opt_diff_override
        print(opt)
        _assert_empty_role2(opt)


class TestNoDiff:  # ===========================================================

    # title  -------------------------------------------------------------------

    def test_sense_title1(_, opt_no_diff):
        opt = opt_no_diff
        print(opt)
        _assert_sense_title1(opt)

    def test_sense_title2(_, opt_no_diff):
        opt = opt_no_diff
        print(opt)
        _assert_sense_title2(opt)

    # diff  --------------------------------------------------------------------

    def test_diff_title(_, opt_no_diff):
        opt = opt_no_diff
        print(opt)
        assert "### sense coder difficulty" in opt

    def test_diff1(_, opt_no_diff):
        opt = opt_no_diff
        print(opt)
        assert "Provide a number between `1` (very easy)" in opt

    def test_diff2(_, opt_no_diff):
        opt = opt_no_diff
        print(opt)
        assert "Use these tasks as your **anchor point**" in opt

    def test_diff3(_, opt_no_diff):
        opt = opt_no_diff
        print(opt)
        assert "- `3` Rename a local variable for clarity" in opt

    def test_diff4(_, opt_no_diff):
        opt = opt_no_diff
        print(opt)
        assert "- `13` Fix basic formatting/indentation or" in opt

    def test_diff5(_, opt_no_diff):
        opt = opt_no_diff
        print(opt)
        assert "- `17` Update a package dependency version" in opt

    def test_diff6(_, opt_no_diff):
        opt = opt_no_diff
        print(opt)
        assert "- `38` Write a simple unit test for a pure" in opt

    def test_diff7(_, opt_no_diff):
        opt = opt_no_diff
        print(opt)
        assert "- `53` Add basic input validation" in opt

    def test_diff8(_, opt_no_diff):
        opt = opt_no_diff
        print(opt)
        assert "- `73` Replace recursion with an iterative" in opt

    def test_diff9(_, opt_no_diff):
        opt = opt_no_diff
        print(opt)
        assert "- `93` Optimize a slow loop by reducing nested" in opt

    def test_diff10(_, opt_no_diff):
        opt = opt_no_diff
        print(opt)
        assert "- `100` Refactor a messy module into smaller" in opt

    # pl -----------------------------------------------------------------------

    def test_pl_instruction_title(_, opt_no_diff):
        opt = opt_no_diff
        print(opt)
        _assert_pl_instruction_title(opt)

    def test_pl_instruction1(_, opt_no_diff):
        opt = opt_no_diff
        print(opt)
        _assert_pl_instruction1(opt)

    def test_pl_instruction2(_, opt_no_diff):
        opt = opt_no_diff
        print(opt)
        _assert_pl_instruction2(opt)

    # plc  ---------------------------------------------------------------------

    def test_plc_title(_, opt_no_diff):
        opt = opt_no_diff
        print(opt)
        _assert_plc_title(opt)

    def test_pl1(_, opt_no_diff):
        opt = opt_no_diff
        print(opt)
        _assert_plc1(opt)

    def test_pl2(_, opt_no_diff):
        opt = opt_no_diff
        print(opt)
        _assert_plc2(opt)

    def test_pl3(_, opt_no_diff):
        opt = opt_no_diff
        print(opt)
        _assert_plc3(opt)

    def test_pl4(_, opt_no_diff):
        opt = opt_no_diff
        print(opt)
        _assert_plc4(opt)

    def test_pl5(_, opt_no_diff):
        opt = opt_no_diff
        print(opt)
        _assert_plc5(opt)

    def test_pl6(_, opt_no_diff):
        opt = opt_no_diff
        print(opt)
        _assert_plc6(opt)

    def test_pl7(_, opt_no_diff):
        opt = opt_no_diff
        print(opt)
        _assert_plc7(opt)

    def test_pl8(_, opt_no_diff):
        opt = opt_no_diff
        print(opt)
        _assert_plc8(opt)

    def test_pl9(_, opt_no_diff):
        opt = opt_no_diff
        print(opt)
        _assert_plc9(opt)

    # empty role  --------------------------------------------------------------

    def test_empty_role1(_, opt_no_diff):
        opt = opt_no_diff
        print(opt)
        _assert_empty_role1(opt)

    def test_empty_role2(_, opt_no_diff):
        opt = opt_no_diff
        print(opt)
        _assert_empty_role2(opt)
