"""
api-ky-sense-coder_test.py

Unit Tests (using pytest) for:

/kaye/dify-app/ky/sense to sense for coder
"""

import pytest


from tests.api.ky.sense import (
    _assert_sense_title1,
    _assert_sense_title2,
    _assert_empty_role1,
    _assert_empty_role2,
)


# Pytest fixtures  #############################################################
@pytest.fixture(scope="class")
def opt_diff_override(flask_test_client, sense_endpoint):
    request_body = {"pre_sense_role": "coder", "difficulty_override": 0}

    response = flask_test_client.post(sense_endpoint, json=request_body)
    return response.get_data().decode("utf-8")


@pytest.fixture(scope="class")
def opt_no_diff(flask_test_client, sense_endpoint):
    request_body = {"pre_sense_role": "coder", "difficulty_override": 15}

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

    # TODO

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

    # TODO

    # empty role  --------------------------------------------------------------

    def test_empty_role1(_, opt_no_diff):
        opt = opt_no_diff
        print(opt)
        _assert_empty_role1(opt)

    def test_empty_role2(_, opt_no_diff):
        opt = opt_no_diff
        print(opt)
        _assert_empty_role2(opt)
