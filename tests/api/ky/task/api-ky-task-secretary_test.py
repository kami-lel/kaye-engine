"""
api-ky-task-secretary_test.py

Unit Tests (using pytest) for:

/kaye/dify-api/ky/task with ?role=secretary
"""

import pytest

from tests.api.ky.task import (
    _assert_rapid_blueprint_opt,
    _assert_good_writing_blueprint_opt,
)


# pytest fixtures  #############################################################
@pytest.fixture
def query_string():
    return {"role": "secretary"}


# pytest  ######################################################################
class TestEditor:

    def test_rapid(_, flask_test_client, task_endpoint, query_string):
        response = flask_test_client.get(
            task_endpoint, query_string=query_string
        )

        opt = response.get_data().decode("utf-8")
        print(opt)

        _assert_rapid_blueprint_opt(opt)

    def test_good_writing(_, flask_test_client, task_endpoint, query_string):
        response = flask_test_client.get(
            task_endpoint, query_string=query_string
        )

        opt = response.get_data().decode("utf-8")
        print(opt)
        _assert_good_writing_blueprint_opt(opt)

    def test1(_, flask_test_client, task_endpoint, query_string):
        response = flask_test_client.get(
            task_endpoint, query_string=query_string
        )

        opt = response.get_data().decode("utf-8")
        print(opt)

        assert """## Secretary
Assist with message-based communication tasks, especially email; act on behalf of the user:

- Draft and compose emails or other messages.
- Extract relevant event information from emails.""" in opt
