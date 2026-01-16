"""
api_dify_kyc_test.py

Unit Tests (using pytest) for: /kaye/dify-app/kyc/*
"""

from kaye.gen_prompt import (
    PromptBlueprint,
    load_embedded_prompt_corpus,
)
from api.dify_app.kaye_peer_coder import PRE_SENSE_PROMPT_BLUEPRINT

APP_PREFIX = "/kaye/dify-app/kyc"


def test_pre_sense(flask_test_client):
    response = flask_test_client.get(APP_PREFIX + "/pre-sense")

    opt = response.data.decode("utf-8")
    print(opt)

    assert (
        opt
        == PromptBlueprint.parse(
            load_embedded_prompt_corpus(), PRE_SENSE_PROMPT_BLUEPRINT
        ).generate_prompt()
    )


def test_chat(flask_test_client):
    response = flask_test_client.get(APP_PREFIX + "/task")
    opt = response.data.decode("utf-8")

    print(opt)
    # TODO
