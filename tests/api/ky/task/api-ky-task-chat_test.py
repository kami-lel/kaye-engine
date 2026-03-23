"""
api-ky-task-chat_test.py

Unit Tests (using pytest) for:

/kaye/dify-api/ky/task with ?role=chat
"""

import pytest

from tests.api.ky.task import _assert_chat_blueprint_opt


# pytest fixtures  #############################################################
@pytest.fixture
def query_string():
    return {"role": "chat"}


class TestChat:  ###############################################################
    # FIXME unit test using json

    # tests  ===================================================================

    def test1(self, flask_test_client, task_endpoint, query_string):
        # should be ignored
        response = flask_test_client.get(
            task_endpoint, query_string=query_string
        )

        opt = response.get_data().decode("utf-8")

        print(opt)
        _assert_chat_blueprint_opt(opt)

    def test_with_pls(self, flask_test_client, task_endpoint, query_string):
        # should be ignored
        query_string["programming_languages"] = "abc"

        response = flask_test_client.get(
            task_endpoint, query_string=query_string
        )
        opt = response.get_data().decode("utf-8")

        print(opt)
        _assert_chat_blueprint_opt(opt)

    def test_no_role(self, flask_test_client, task_endpoint):
        response = flask_test_client.get(
            task_endpoint,
        )

        opt = response.get_data().decode("utf-8")

        print(opt)
        _assert_chat_blueprint_opt(opt)

    def test_empty_role(self, flask_test_client, task_endpoint, query_string):
        query_string = {"role": ""}

        response = flask_test_client.get(
            task_endpoint, query_string=query_string
        )
        opt = response.get_data().decode("utf-8")

        print(opt)
        _assert_chat_blueprint_opt(opt)
