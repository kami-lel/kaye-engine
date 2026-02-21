"""
api_dify_ky_test.py

Unit Tests (using pytest) for: /kaye/dify-app/ky/*
"""

# HACK rm

from kaye.prompt import (
    PromptBlueprint,
    load_embedded_prompt_corpus,
    load_embedded_prompt_blueprint,
)
from api.dify_app.kaye_chat import PRE_SENSE_PROMPT_BLUEPRINT

APP_PREFIX = "/kaye/dify-app/ky"


def test_task(flask_test_client):
    response = flask_test_client.get(APP_PREFIX + "/chat")

    opt = response.data.decode("utf-8")
    print(opt)

    assert opt == load_embedded_prompt_blueprint("chat").generate_prompt()
