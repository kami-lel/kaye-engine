"""
api-ky-task-rapid_test.py

Unit Tests (using pytest) for:

/kaye/dify-api/ky/task with role=rapid
"""

import pytest


# pytest fixtures  #############################################################
@pytest.fixture
def local_query_string_base():
    return {"role": "aaa"}


class TestRapid:

    def test1(self, flask_test_client, task_endpoint, local_query_string_base):
        query_string = local_query_string_base
        response = flask_test_client.get(
            task_endpoint, query_string=query_string
        )

        opt = response.get_data().decode("utf-8")

        print(opt)
        assert opt.startswith("aa")
        assert opt.endswith("dd")

    # TODO
