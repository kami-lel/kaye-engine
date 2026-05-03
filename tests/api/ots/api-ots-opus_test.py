"""
api-ots-opus_test.py

Unit Tests (using pytest) for:

/kaye/dify-app/opus-tag-smith/opus
"""

import pytest

# Pytest fixtures  #############################################################


@pytest.fixture(scope="class")
def opt(flask_test_client, dify_app_endpoint):
    endpoint = dify_app_endpoint + "/opus-tag-smith/opus"
    response = flask_test_client.get(endpoint)
    return response.get_data().decode("utf-8")


# Pytest unit tests  ###########################################################


class TestOpus:

    # TODO unit test for tag smith extract prompt

    def test_title0(_, opt, main0):
        print(opt)
        assert main0 in opt

    def test_extract0(_, opt, title0):
        assert title0 in opt

    def test_tags0(_, opt, tags0):
        print(opt)
        assert tags0 in opt
