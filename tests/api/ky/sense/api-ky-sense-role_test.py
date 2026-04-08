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

    def test1(_):
        pass  # TODO

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
