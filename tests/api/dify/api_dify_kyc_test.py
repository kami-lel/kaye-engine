"""
api_dify_kyc_test.py

Unit Tests (using pytest) for: /kaye/dify-app/kyc/*
"""

from kaye.gen_prompt import (
    PromptBlueprint,
    load_embedded_prompt_corpus,
)
from api.dify_app.kaye_peer_coder import (
    PRE_SENSE_PROMPT_BLUEPRINT,
    CHAT_PROMPT_BASIC_BLUEPRINT,
)

APP_PREFIX = "/kaye/dify-app/kyc"
CHAT_ENDPOINT = APP_PREFIX + "/chat"


# test /pre-sense  #############################################################
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


# test /chat  ##################################################################


def test_chat_basic(flask_test_client):
    response = flask_test_client.get(CHAT_ENDPOINT)
    opt = response.data.decode("utf-8")

    opt = response.data.decode("utf-8")
    print(opt)

    assert (
        opt
        == PromptBlueprint.parse(
            load_embedded_prompt_corpus(), CHAT_PROMPT_BASIC_BLUEPRINT
        ).generate_prompt()
    )


# TODO test params
