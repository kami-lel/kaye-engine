"""
api-ky-sense-diff_test.py

Unit Tests (using pytest) for:

/kaye/dify-app/ky/sense to sense for difficulty (only)
"""

import pytest

from tests.api.ky.sense import *

# Pytest fixtures  #############################################################


@pytest.fixture(scope="class")
def opt(flask_test_client, sense_endpoint):
    request_body = {"pre_sense_role": "chat", "difficulty_override": 0}

    response = flask_test_client.post(sense_endpoint, json=request_body)
    return response.get_data().decode("utf-8")


# Pytest unit tests  ###########################################################


class TestDiff:  # =============================================================

    # title  -------------------------------------------------------------------

    def test_sense_title1(_, opt):
        print(opt)
        assert_sense_title1(opt)

    def test_sense_title2(_, opt):
        print(opt)
        assert_sense_title2(opt)

    # diff  --------------------------------------------------------------------

    def test_title1(_, opt):
        print(opt)
        assert_diff_title(opt)

    def test1(_, opt):
        print(opt)
        assert_diff1(opt)

    def test2(_, opt):
        print(opt)
        assert_diff2(opt)

    def test3(_, opt):
        print(opt)
        assert_diff3(opt)

    def test4(_, opt):
        print(opt)
        assert_diff4(opt)

    def test5(_, opt):
        print(opt)
        assert_diff5(opt)

    def test6(_, opt):
        print(opt)
        assert_diff6(opt)

    def test7(_, opt):
        print(opt)
        assert_diff7(opt)

    # empty role  --------------------------------------------------------------

    def test_empty_role1(_, opt):
        print(opt)
        assert_empty_role1(opt)

    def test_empty_role2(_, opt):
        print(opt)
        assert_empty_role2(opt)

    # empty PLs  ---------------------------------------------------------------

    def test_empty_pls1(_, opt):
        print(opt)
        assert_empty_pls1(opt)

    def test_empty_pls2(_, opt):
        print(opt)
        assert_empty_pls2(opt)
