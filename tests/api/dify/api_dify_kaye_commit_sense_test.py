"""
api_dify_kaye_commit_sense_test.py

Unit Tests (using pytest) for: /kaye/dify-app/kaye-commit-sense/*
"""

from kaye.gen_prompt import load_embedded_prompt_corpus, PromptBlueprint
from api.dify_app.kaye_commit_sense import (
    PRIMARY_MESSAGE_PROMPT_BLUEPRINT,
    PER_FILE_LONG_PROMPT_BLUEPRINT,
    PER_FILE_SHORT_PROMPT_BLUEPRINT,
)

APP_PREFIX = "/kaye/dify-app/kaye-commit-sense"


def test_primary_message(flask_test_client):
    response = flask_test_client.get(APP_PREFIX + "/primary-message")

    opt = response.data.decode("utf-8")
    print(opt)

    assert (
        opt
        == PromptBlueprint.parse(
            load_embedded_prompt_corpus(), PRIMARY_MESSAGE_PROMPT_BLUEPRINT
        ).generate_prompt()
    )


def test_per_file_long(flask_test_client):
    response = flask_test_client.get(APP_PREFIX + "/per-file-long")

    opt = response.data.decode("utf-8")
    print(opt)

    assert (
        opt
        == PromptBlueprint.parse(
            load_embedded_prompt_corpus(), PER_FILE_LONG_PROMPT_BLUEPRINT
        ).generate_prompt()
    )


def test_per_file_short(flask_test_client):
    response = flask_test_client.get(APP_PREFIX + "/per-file-short")

    opt = response.data.decode("utf-8")
    print(opt)

    assert (
        opt
        == PromptBlueprint.parse(
            load_embedded_prompt_corpus(), PER_FILE_SHORT_PROMPT_BLUEPRINT
        ).generate_prompt()
    )


# TODO tests for params
