"""
api-ky-task-rapid_test.py

Unit Tests (using pytest) for:

/kaye/dify-api/ky/task with role=rapid
"""

import json


from tests.api.ky.task import _assert_rapid_blueprint_opt


class TestRapid:  ##############################################################

    # tests  ===================================================================

    def test1(self, flask_test_client, task_endpoint):
        payload = json.dumps({"role": "rapid"})

        response = flask_test_client.post(
            task_endpoint,
            data=payload,
            content_type="application/json",
        )

        opt = response.get_data().decode("utf-8")

        print(opt)
        _assert_rapid_blueprint_opt(opt)

    def test_with_pls(self, flask_test_client, task_endpoint):
        payload = json.dumps({"role": "rapid", "programming_languages": "abc"})

        response = flask_test_client.post(
            task_endpoint,
            data=payload,
            content_type="application/json",
        )

        opt = response.get_data().decode("utf-8")

        print(opt)
        _assert_rapid_blueprint_opt(opt)
