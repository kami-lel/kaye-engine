"""
api-ky-merge_test.py

Unit Tests (using pytest) for:

/kaye/dify-app/ky/merge
"""

# Pytest unit tests  ###########################################################


def test_merge(flask_test_client, app_endpoint):
    merge_endpoint = app_endpoint + "/merge"

    response = flask_test_client.get(merge_endpoint)
    opt = response.get_data().decode("utf-8")

    # TODO unit test
