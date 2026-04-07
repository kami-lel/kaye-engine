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

    print(opt)
    assert "# Kaye Chat" in opt
    assert "## merge" in opt
    assert "You will receive multiple answers to the same question." in opt
    assert "Synthesize all provided answers into one" in opt
    assert "Output only the merged answer" in opt
