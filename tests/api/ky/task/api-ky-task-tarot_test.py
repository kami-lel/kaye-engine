"""
api-ky-task-tarot_test.py

Unit Tests (using pytest) for:

/kaye/dify-api/ky/task with role=tarot
"""

import json


import pytest


from tests.api.ky.task import _assert_rapid_blueprint_opt


# pytest fixtures  #############################################################
@pytest.fixture
def payload_json_dumps():
    payload = {"role": "tarot"}
    return json.dumps(payload)


# Pytest unit tests  ###########################################################
# TODO unit test
