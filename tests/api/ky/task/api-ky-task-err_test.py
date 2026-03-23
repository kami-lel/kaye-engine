"""
api-ky-task-err_test.py

Unit Tests (using pytest) for:

errors of /kaye/dify-api/ky/task
"""

# BUG


class TestErrRole:

    def test1(self, flask_test_client, task_endpoint):
        query_string = {"role": "abc"}
        response = flask_test_client.get(
            task_endpoint, query_string=query_string
        )

        opt = response.get_data(as_text=True)

        assert response._status_code == 422
        assert opt == "bad param: ?role=abc"
