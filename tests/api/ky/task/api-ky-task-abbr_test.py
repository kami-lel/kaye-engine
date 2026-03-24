"""
api-ky-task-abbr_test.py

Unit Tests (using pytest) for:

/kaye/dify-api/ky/task with abbreviations
"""

import json

# pytest  ######################################################################


class TestSingle:  # ===========================================================

    def test1(self, flask_test_client, task_endpoint):
        query = "abc def"
        payload = {"role": "rapid", "query": query}

        response = flask_test_client.get(
            task_endpoint,
            data=json.dumps(payload),
            content_type="application/json",
        )

        opt = response.get_data().decode("utf-8")

        print(opt)
        assert opt.startswith(self.answer_start)
        assert opt.endswith(self.answer_end)

    # TODO unit test


class TestMux:  # ==============================================================

    def test1(_):
        pass
