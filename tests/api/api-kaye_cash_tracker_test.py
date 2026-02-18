"""
api_dify_kaye_cash_tracker_test.py

Unit Tests (using pytest) for: /kaye/dify-app/kaye-cash-tracker/*
"""

from kaye.prompt import (
    PromptBlueprint,
    load_embedded_prompt_corpus,
)
from api.dify_app.kaye_cash_tracker import EXTRACT_PROMPT_BLUEPRINT


def test_extract(flask_test_client):
    response = flask_test_client.get("/kaye/dify-app/kaye-cash-tracker/extract")

    opt = response.data.decode("utf-8")
    print(opt)

    assert opt == PromptBlueprint.parse(
        load_embedded_prompt_corpus(), EXTRACT_PROMPT_BLUEPRINT
    ).generate_prompt(hide_comment=False)
