"""
api-ky-sense-diff_test.py

Unit Tests (using pytest) for:

/kaye/dify-app/ky/sense to sense for difficulty (only)
"""

import pytest

from tests.api.ky.sense import (
    _assert_empty_role1,
    _assert_empty_role2,
    _assert_empty_pls1,
    _assert_empty_pls2,
)

# Pytest fixtures  #############################################################


@pytest.fixture(scope="class")
def opt(flask_test_client, sense_endpoint):
    request_body = {"pre_sense_role": "chat", "difficulty_override": 0}
    response = flask_test_client.post(sense_endpoint, json=request_body)
    return response.get_data().decode("utf-8")


# Pytest unit tests  ###########################################################


class TestDiff:

    def test_title1(_, opt):
        print(opt)
        assert "### sense difficulty" in opt

    def test1(_, opt):
        print(opt)
        assert "Provide a number between `1` (very easy)" in opt

    def test2(_, opt):
        print(opt)
        assert "Use these tasks as your **anchor point**" in opt

    def test3(_, opt):
        print(opt)
        assert "- `3` Correct a single typo or awkward word " in opt

    def test4(_, opt):
        print(opt)
        assert "- `50` Fix a misunderstanding caused by missing" in opt

    def test5(_, opt):
        print(opt)
        assert "- `75` Choose and apply an appropriate common" in opt

    def test6(_, opt):
        print(opt)
        assert "- `96` Integrate a standard external source" in opt

    def test7(_, opt):
        print(opt)
        assert "- `100` Refactor a messy, ambiguous" in opt

    def test_empty_role1(_, opt):
        print(opt)
        _assert_empty_role1(opt)

    def test_empty_role2(_, opt):
        print(opt)
        _assert_empty_role2(opt)

    def test_empty_pls1(_, opt):
        print(opt)
        _assert_empty_pls1(opt)

    def test_empty_pls2(_, opt):
        print(opt)
        _assert_empty_pls2(opt)
