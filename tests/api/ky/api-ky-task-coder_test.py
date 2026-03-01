"""
api-ky-task-coder_test.py

Unit Tests (using pytest) for:

/kaye/dify-api/ky/task with ?role=peer_coder
"""

import pytest

from tests.api.ky import _assert_chat_blueprint_opt


# pytest fixtures  #############################################################
@pytest.fixture
def query_string():
    return {"role": "peer_coder"}


class TestBase:  ###############################################################

    def assert_opt(_, opt):
        _assert_chat_blueprint_opt(opt)
        # TODO more tests

    def test_no_plc(self, flask_test_client, task_endpoint, query_string):
        response = flask_test_client.get(
            task_endpoint, query_string=query_string
        )

        opt = response.get_data().decode("utf-8")
        print(opt)

        self.assert_opt(opt)

    def test_empty_plc1(self, flask_test_client, task_endpoint, query_string):
        query_string["programming_languages"] = ""
        response = flask_test_client.get(
            task_endpoint, query_string=query_string
        )

        opt = response.get_data().decode("utf-8")
        print(opt)

        self.assert_opt(opt)

    def test_empty_plc2(self, flask_test_client, task_endpoint, query_string):
        query_string["programming_languages"] = ","
        response = flask_test_client.get(
            task_endpoint, query_string=query_string
        )

        opt = response.get_data().decode("utf-8")
        print(opt)

        self.assert_opt(opt)
