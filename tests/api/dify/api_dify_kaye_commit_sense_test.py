"""
api_dify_kaye_commit_sense_test.py

Unit Tests (using pytest) for: /kaye/dify-app/kaye-commit-sense/*
"""

APP_PREFIX = "/kaye/dify-app/kaye-commit-sense"


def test_primary_message(flask_app):
    # BUG
    response = flask_app.get(APP_PREFIX + "/primary-message")
    assert "a" in response.data
