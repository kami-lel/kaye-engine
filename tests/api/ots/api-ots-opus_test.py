"""
api-ots-opus_test.py

Unit Tests (using pytest) for:

/kaye/dify-app/opus-tag-smith/opus
"""

import pytest

# Pytest fixtures  #############################################################


@pytest.fixture(scope="class")
def decoded_response(flask_test_client, dify_app_endpoint):
    endpoint = dify_app_endpoint + "/opus-tag-smith/opus"
    response = flask_test_client.get(endpoint)
    return response.get_data().decode("utf-8")


# Pytest unit tests  ###########################################################


class TestOpus:

    def test1(_):
        assert False
        pass  # TODO unit test for tag smith extract prompt
