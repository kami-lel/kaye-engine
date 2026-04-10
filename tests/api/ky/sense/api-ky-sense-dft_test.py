"""
api-ky-sense-dft_test.py

Unit Tests (using pytest) for:

/kaye/dify-app/ky/sense with missing entry in request body
"""

import pytest

from tests.api.ky.sense import *

# Pytest fixtures  #############################################################


@pytest.fixture(scope="class")
def opt(flask_test_client, sense_endpoint):
    request_body = {}

    response = flask_test_client.post(sense_endpoint, json=request_body)
    return response.get_data().decode("utf-8")


# Pytest unit tests  ###########################################################


class TestBoth:  # =============================================================

    # title  -------------------------------------------------------------------

    def test_sense_title1(_, opt):
        print(opt)
        assert_sense_title1(opt)

    def test_sense_title2(_, opt):
        print(opt)
        assert_sense_title2(opt)

    # role  --------------------------------------------------------------------

    def test_sense_role_title1(_, opt):
        print(opt)
        assert_role_title(opt)

    def test_role1(_, opt):
        print(opt)
        assert_role1(opt)

    def test_role2(_, opt):
        print(opt)
        assert_role2(opt)

    def test_role3(_, opt):
        print(opt)
        assert_role3(opt)

    def test_role4(_, opt):
        print(opt)
        assert_role4(opt)

    def test_role5(_, opt):
        print(opt)
        assert_role5(opt)

    def test_role6(_, opt):
        print(opt)
        assert_role6(opt)

    def test_role7(_, opt):
        print(opt)
        assert_role7(opt)

    # diff  --------------------------------------------------------------------

    def test_title1(_, opt):
        print(opt)
        assert_diff_title(opt)

    def test_diff1(_, opt):
        print(opt)
        assert_diff1(opt)

    def test_diff2(_, opt):
        print(opt)
        assert_diff2(opt)

    def test_diff3(_, opt):
        print(opt)
        assert_diff3(opt)

    def test_diff4(_, opt):
        print(opt)
        assert_diff4(opt)

    def test_diff5(_, opt):
        print(opt)
        assert_diff5(opt)

    def test_diff6(_, opt):
        print(opt)
        assert_diff6(opt)

    def test_diff7(_, opt):
        print(opt)
        assert_diff7(opt)

    # empty PLs  ---------------------------------------------------------------

    def test_empty_pls1(_, opt):
        print(opt)
        assert_empty_pls1(opt)

    def test_empty_pls2(_, opt):
        print(opt)
        assert_empty_pls2(opt)
