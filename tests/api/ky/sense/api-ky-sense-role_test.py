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
    _assert_role_title,
    _assert_role1,
    _assert_role2,
    _assert_role3,
    _assert_role4,
    _assert_role5,
    _assert_role6,
    _assert_role7,
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
        _assert_role_title(opt)

    def test1(_, opt):
        print(opt)
        _assert_role1(opt)

    def test2(_, opt):
        print(opt)
        _assert_role2(opt)

    def test3(_, opt):
        print(opt)
        _assert_role3(opt)

    def test4(_, opt):
        print(opt)
        _assert_role4(opt)

    def test5(_, opt):
        print(opt)
        _assert_role5(opt)

    def test6(_, opt):
        print(opt)
        _assert_role6(opt)

    def test7(_, opt):
        print(opt)
        _assert_role7(opt)

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
