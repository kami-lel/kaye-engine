"""
api-ky-task-barista_test.py

Unit Tests (using pytest) for:

/kaye/dify-api/ky/task with ?role=barista
"""

import pytest


# pytest fixtures  #############################################################
@pytest.fixture
def query_string():
    return {"role": "barista"}


# pytest  ######################################################################
class TestBarista:

    def test1(_, flask_test_client, task_endpoint, query_string):
        response = flask_test_client.get(
            task_endpoint,
        )

        opt = response.get_data().decode("utf-8")

        print(opt)

        assert """""" in opt  # HACK
