"""
api-ky-merge_test.py

Unit Tests (using pytest) for:

/kaye/dify-app/ky/merge
"""

# Pytest unit tests  ###########################################################


def test_merge(flask_test_client, sense_endpoint):
    response = flask_test_client.get()
    opt = response.get_data().decode("utf-8")

    # TODO unit test
