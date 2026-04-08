"""
api-ky-task-chat1_test.py

Unit Tests (using pytest) for:

/kaye/dify-api/ky/task with:

- role=chat
- no PLs
"""

import json

import pytest

# Pytest fixtures  #############################################################


@pytest.fixture(scope="class")
def opt(flask_test_client, task_endpoint):
    payload = json.dumps({"role": "chat"})

    response = flask_test_client.post(
        task_endpoint,
        data=payload,
        content_type="application/json",
    )

    return response.get_data().decode("utf-8")


# Pytest unit tests  ###########################################################


class TestChat:  # =============================================================

    pass  # TODO
