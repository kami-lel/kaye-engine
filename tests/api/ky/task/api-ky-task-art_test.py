"""
api-ky-task-art_test.py

Unit Tests (using pytest) for:

/kaye/dify-api/ky/task with role=art
"""

import json


import pytest


from tests.api.ky.task import _assert_rapid_blueprint_opt

# pytest fixtures  #############################################################


@pytest.fixture(scope="class")
def post_result(flask_test_client, task_endpoint):
    payload_json_dumps = json.dumps({"role": "art"})

    response = flask_test_client.post(
        task_endpoint,
        data=payload_json_dumps,
        content_type="application/json",
    )

    opt = response.get_data().decode("utf-8")

    return opt


# Pytest unit tests  ###########################################################
class TestArt:

    def test_rapid(_, post_result):
        opt = post_result
        print(opt)
        _assert_rapid_blueprint_opt(opt)

    def test1(_, post_result):
        opt = post_result
        print(opt)

        assert "## Art Tutor" in opt

    def test2(_, post_result):
        opt = post_result
        print(opt)

        assert "Your role is to help users craft detailed" in opt

    def test3(_, post_result):
        opt = post_result
        print(opt)

        assert "#### A: Information Gathering" in opt

    def test4(_, post_result):
        opt = post_result
        print(opt)

        assert "#### B: Prompt Generation" in opt
