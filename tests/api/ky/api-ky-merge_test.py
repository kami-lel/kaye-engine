"""
api-ky-merge_test.py

Unit Tests (using pytest) for:

/kaye/dify-app/ky/merge
"""

import pytest

# helpers  #####################################################################


def _assert_title1(opt):
    assert "# Kaye Chat" in opt


# Pytest fixtures  #############################################################
@pytest.fixture
def opt(flask_test_client, app_endpoint):
    merge_endpoint = app_endpoint + "/merge"

    response = flask_test_client.get(merge_endpoint)
    return response.get_data().decode("utf-8")


# Pytest unit tests  ###########################################################
class TestMerge:

    def test_title1(_, opt):
        print(opt)
        assert "# Kaye Chat" in opt

    def test_title2(_, opt):
        print(opt)
        assert "## merge" in opt

    def test1(_, opt):
        print(opt)
        assert "You will receive multiple answers to the same question." in opt

    def test2(_, opt):
        print(opt)
        assert "Synthesize all provided answers into one" in opt

    def test3(_, opt):
        print(opt)
        assert "Output only the merged answer" in opt
