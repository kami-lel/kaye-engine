"""
api-dify_kaye_cash_tracker_test.py

Unit Tests (using pytest) for: /kaye/dify-app/kaye-cash-tracker/*
"""


def test_extract(flask_test_client, dify_app_endpoint):
    extract_endpoint = dify_app_endpoint + "/kaye-cash-tracker/extract"

    response = flask_test_client.get(extract_endpoint)

    opt = response.get_data().decode("utf-8")
    print(opt)

    assert False

    # BUG commit sense API
