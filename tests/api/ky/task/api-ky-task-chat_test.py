"""
api-ky-task-chat_test.py

Unit Tests (using pytest) for:

/kaye/dify-api/ky/task with role=chat
"""

import json


from tests.api.ky.task import _assert_chat_blueprint_opt


class TestChat:  ###############################################################

    # tests  ===================================================================

    def test1(self, flask_test_client, task_endpoint):
        # should be ignored
        payload = {"role": "chat"}

        response = flask_test_client.get(
            task_endpoint,
            data=json.dumps(payload),
            content_type="application/json",
        )

        opt = response.get_data().decode("utf-8")

        print(opt)
        _assert_chat_blueprint_opt(opt)

    def test_with_pls(self, flask_test_client, task_endpoint):
        # should be ignored
        payload = {"role": "chat", "programming_languages": "abc"}

        response = flask_test_client.get(
            task_endpoint,
            data=json.dumps(payload),
            content_type="application/json",
        )

        opt = response.get_data().decode("utf-8")

        print(opt)
        _assert_chat_blueprint_opt(opt)

    def test_no_role(self, flask_test_client, task_endpoint):
        response = flask_test_client.get(task_endpoint)

        opt = response.get_data().decode("utf-8")

        print(opt)
        _assert_chat_blueprint_opt(opt)

    def test_empty_role(self, flask_test_client, task_endpoint):
        payload = {"role": ""}

        response = flask_test_client.get(
            task_endpoint,
            data=json.dumps(payload),
            content_type="application/json",
        )

        opt = response.get_data().decode("utf-8")

        print(opt)
        _assert_chat_blueprint_opt(opt)
