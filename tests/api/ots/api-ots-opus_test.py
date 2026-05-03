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

    def test_main0(_, opt, main0):
        assert main0 in opt

    def test_main1(_, opt, main1):
        assert main1 in opt

    def test_main2(_, opt, main2):
        assert main2 in opt

    def test_main3(_, opt, main3):
        assert main3 in opt

    def test_title0(_, opt, title0):
        assert title0 in opt

    def test_title1(_, opt, title1):
        assert title1 in opt

    def test_title2(_, opt, title2):
        assert title2 in opt

    def test_title3(_, opt, title3):
        assert title3 in opt

    def test_title4(_, opt, title4):
        assert title4 in opt

    def test_tags0(_, opt, tags0):
        print(opt)
        assert tags0 in opt

    def test_tag_instruction1(_, opt, tag_instruction1):
        print(opt)
        assert tag_instruction1 in opt

    def test_tag_instruction2(_, opt, tag_instruction2):
        print(opt)
        assert tag_instruction2 in opt

    def test_tag_instruction3(_, opt, tag_instruction3):
        print(opt)
        assert tag_instruction3 in opt

    def test_tag_instruction4(_, opt, tag_instruction4):
        print(opt)
        assert tag_instruction4 in opt

    def test_tags1(_, opt, tags1):
        print(opt)
        assert tags1 in opt

    def test_tags2(_, opt, tags2):
        print(opt)
        assert tags2 in opt
