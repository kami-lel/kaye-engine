"""
api-ky-sense-diff_test.py

Unit Tests (using pytest) for:

/kaye/dify-app/ky/sense to sense for difficulty (only)
"""

import pytest

# Pytest fixtures  #############################################################


@pytest.fixture(scope="class")
def opt(flask_test_client, sense_endpoint):
    request_body = {"pre_sense_role": "chat", "difficulty_override": 0}
    response = flask_test_client.post(sense_endpoint, json=request_body)
    return response.get_data().decode("utf-8")


# Pytest unit tests  ###########################################################


class TestDiff:

    def test_title1(_, opt):
        assert "### sense difficulty" in opt

    def test1(_, opt):
        assert "Provide a number between `1` (very easy)" in opt

    def test2(_, opt):
        assert "Use these tasks as your **anchor point**" in opt

    def test3(_, opt):
        assert "- `3` Correct a single typo or awkward word " in opt

    def test4(_, opt):
        assert "- `50` Fix a misunderstanding caused by missing" in opt

    def test5(_, opt):
        assert "- `75` Choose and apply an appropriate common" in opt

    def test6(_, opt):
        assert "- `96` Integrate a standard external source" in opt

    def test7(_, opt):
        assert "- `100` Refactor a messy, ambiguous" in opt


# TODO
