"""
api-ky-sense-role_test.py

Unit Tests (using pytest) for:

/kaye/dify-app/ky/sense to sense for role (only)
"""

import pytest

from tests.api.ky.sense import (
    _assert_sense_title1,
    _assert_sense_title2,
    _assert_zero_diff1,
    _assert_zero_diff2,
    _assert_empty_pls1,
    _assert_empty_pls2,
)

# Pytest fixtures  #############################################################


@pytest.fixture(scope="class")
def opt(flask_test_client, sense_endpoint):
    request_body = {"pre_sense_role": "", "difficulty_override": 15}

    response = flask_test_client.post(sense_endpoint, json=request_body)
    return response.get_data().decode("utf-8")


# Pytest unit tests  ###########################################################


class TestRole:

    def test_sense_title1(_, opt):
        print(opt)
        _assert_sense_title1(opt)

    def test_sense_title2(_, opt):
        print(opt)
        _assert_sense_title2(opt)

    def test_sense_role_title1(_, opt):
        print(opt)
        assert "### sense role" in opt

    def test1(_, opt):
        print(opt)
        assert "select exactly one role. choose the" in opt

    def test2(_, opt):
        print(opt)
        assert "- `art`: when the user gives you **a visual idea for" in opt

    def test3(_, opt):
        print(opt)
        assert "- `changelog`: when the user gives you **changelog or" in opt

    def test4(_, opt):
        print(opt)
        assert "- `chat`: when the user gives you a **general question" in opt

    def test5(_, opt):
        print(opt)
        assert "- `coder`: when the user gives you **code or" in opt

    def test6(_, opt):
        print(opt)
        assert "- `librarian`: when the user gives you **a text to read" in opt

    def test7(_, opt):
        print(opt)
        assert "- `secretary`: when the user gives you" in opt

    def test_zero_diff1(_, opt):
        print(opt)
        _assert_zero_diff1(opt)

    def test_zero_diff2(_, opt):
        print(opt)
        _assert_zero_diff2(opt)

    def test_empty_pls1(_, opt):
        print(opt)
        _assert_empty_pls1(opt)

    def test_empty_pls2(_, opt):
        print(opt)
        _assert_empty_pls2(opt)
