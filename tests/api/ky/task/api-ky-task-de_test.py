"""
api-ky-task-de_test.py

Unit Tests (using pytest) for:

/kaye/dify-api/ky/task with role=deutschlehrer
"""

import json


import pytest


from tests.api.ky.task import _assert_rapid_blueprint_opt

# pytest fixtures  #############################################################


@pytest.fixture(scope="class")
def post_result(flask_test_client, task_endpoint):
    payload_json_dumps = json.dumps({"role": "deutschlehrer"})

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

    def test_title(_, post_result):
        opt = post_result
        print(opt)

        assert "## Deutschlehrer" in opt

    def test2(_, post_result):
        opt = post_result
        print(opt)

        assert "You perform **Deutschlehrer** role to assist" in opt

    def test3(_, post_result):
        opt = post_result
        print(opt)

        assert "Die Atmosphäre ist lebhaft und bunt" in opt

    def test4(_, post_result):
        opt = post_result
        print(opt)

        assert "</example-response3>" in opt
