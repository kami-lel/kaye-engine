"""
api-ky-task-tarot_test.py

Unit Tests (using pytest) for:

/kaye/dify-api/ky/task with role=tarot
"""

import json


import pytest


from tests.api.ky.task import _assert_rapid_blueprint_opt

# pytest fixtures  #############################################################


@pytest.fixture(scope="class")
def post_result(flask_test_client, task_endpoint):
    payload_json_dumps = json.dumps({"role": "tarot"})

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

        assert "## Tarot Reader" in opt

    def test1(_, post_result):
        opt = post_result
        print(opt)

        assert "### 1. Information Collection Stage" in opt

    def test2(_, post_result):
        opt = post_result
        print(opt)

        assert "- Begin with a casual conversation to" in opt

    def test3(_, post_result):
        opt = post_result
        print(opt)

        assert "### 2. Card Drawing Stage" in opt

    def test4(_, post_result):
        opt = post_result
        print(opt)

        assert "- Randomly select 3 **unique** cards from" in opt

    def test5(_, post_result):
        opt = post_result
        print(opt)

        assert "and explain how each card might answer" in opt

    def test6(_, post_result):
        opt = post_result
        print(opt)

        assert "### 3. Interpretation Stage" in opt

    def test7(_, post_result):
        opt = post_result
        print(opt)

        assert "In this ongoing conversation" in opt

    def test8(_, post_result):
        opt = post_result
        print(opt)

        assert "### Tarot Card Reference" in opt

    def test9(_, post_result):
        opt = post_result
        print(opt)

        assert "67. Three of Pentacles" in opt
