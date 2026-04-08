"""
api-ky-sense-both_test.py

Unit Tests (using pytest) for:

/kaye/dify-app/ky/sense to sense for role & difficulty
"""

import pytest

from tests.api.ky.sense import (
    _assert_sense_title1,
    _assert_sense_title2,
    _assert_empty_pls1,
    _assert_empty_pls2,
)

# Pytest fixtures  #############################################################


@pytest.fixture(scope="class")
def opt(flask_test_client, sense_endpoint):
    request_body = {"pre_sense_role": "", "difficulty_override": 0}

    response = flask_test_client.post(sense_endpoint, json=request_body)
    return response.get_data().decode("utf-8")


# Pytest unit tests  ###########################################################


class TestBoth:

    def test_sense_title1(_, opt):
        print(opt)
        _assert_sense_title1(opt)

    def test_sense_title2(_, opt):
        print(opt)
        _assert_sense_title2(opt)

    # TODO both

    def test_empty_pls1(_, opt):
        print(opt)
        _assert_empty_pls1(opt)

    def test_empty_pls2(_, opt):
        print(opt)
        _assert_empty_pls2(opt)
