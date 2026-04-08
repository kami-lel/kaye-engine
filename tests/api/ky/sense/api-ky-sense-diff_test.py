"""
api-ky-sense-diff_test.py

Unit Tests (using pytest) for:

/kaye/dify-app/ky/sense to sense for difficulty (only)
"""

import pytest

from tests.api.ky.sense import (
    _assert_sense_title1,
    _assert_sense_title2,
    _assert_empty_role1,
    _assert_empty_role2,
    _assert_empty_pls1,
    _assert_empty_pls2,
    _assert_diff_title,
    _assert_diff1,
    _assert_diff2,
    _assert_diff3,
    _assert_diff4,
    _assert_diff5,
    _assert_diff6,
    _assert_diff7,
)

# Pytest fixtures  #############################################################


@pytest.fixture(scope="class")
def opt(flask_test_client, sense_endpoint):
    request_body = {"pre_sense_role": "chat", "difficulty_override": 0}

    response = flask_test_client.post(sense_endpoint, json=request_body)
    return response.get_data().decode("utf-8")


# Pytest unit tests  ###########################################################


class TestDiff:

    def test_sense_title1(_, opt):
        print(opt)
        _assert_sense_title1(opt)

    def test_sense_title2(_, opt):
        print(opt)
        _assert_sense_title2(opt)

    def test_title1(_, opt):
        print(opt)
        _assert_diff_title(opt)

    def test1(_, opt):
        print(opt)
        _assert_diff1(opt)

    def test2(_, opt):
        print(opt)
        _assert_diff2(opt)

    def test3(_, opt):
        print(opt)
        _assert_diff3(opt)

    def test4(_, opt):
        print(opt)
        _assert_diff4(opt)

    def test5(_, opt):
        print(opt)
        _assert_diff5(opt)

    def test6(_, opt):
        print(opt)
        _assert_diff6(opt)

    def test7(_, opt):
        print(opt)
        _assert_diff7(opt)

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
