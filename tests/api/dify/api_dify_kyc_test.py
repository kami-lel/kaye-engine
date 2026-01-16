"""
api_dify_kyc_test.py

Unit Tests (using pytest) for: /kaye/dify-app/kyc/*
"""

import json

from kaye.gen_prompt import (
    PromptBlueprint,
    load_embedded_prompt_corpus,
)
from api.dify_app.kaye_peer_coder import (
    PRE_SENSE_PROMPT_BLUEPRINT,
    CHAT_PROMPT_BASIC_BLUEPRINT,
    PL,
)
from tests import _print_heading

APP_PREFIX = "/kaye/dify-app/kyc"


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

CHAT_ENDPOINT = APP_PREFIX + "/chat"
CHAT_BASIC_PROMPT = PromptBlueprint.parse(
    load_embedded_prompt_corpus(), CHAT_PROMPT_BASIC_BLUEPRINT
).generate_prompt(hide_comment=True)


class TestChatBasic:  # ========================================================

    def test_no_param(self, flask_test_client):
        response = flask_test_client.get(CHAT_ENDPOINT)
        flags, prompt = _deconstruct_chat_response(response)

        _print_heading("flags")
        print(flags)
        _print_heading("prompt")
        print(prompt)

        assert flags == PL.NONE
        assert CHAT_BASIC_PROMPT in prompt

    def test_empty_param(self, flask_test_client):
        flags = PL.NONE
        lang_param = ""

        flags_param = int(flags)
        response = flask_test_client.get(
            CHAT_ENDPOINT
            + "?flags={}&languages={}".format(flags_param, lang_param)
        )
        flags, prompt = _deconstruct_chat_response(response)

        _print_heading("flags")
        print(flags)
        _print_heading("prompt")
        print(prompt)

        assert flags == PL.NONE
        assert CHAT_BASIC_PROMPT in prompt


class TestChatLanguages:  # fx of languages  ===================================

    def test1(self, flask_test_client):
        flags = PL.NONE
        lang_param = "cpp"

        flags_param = int(flags)
        response = flask_test_client.get(
            CHAT_ENDPOINT
            + "?flags={}&languages={}".format(flags_param, lang_param)
        )
        flags, prompt = _deconstruct_chat_response(response)

        _print_heading("flags")
        print(flags)
        _print_heading("prompt")
        print(prompt)

        assert flags == PL.cpp
        assert CHAT_BASIC_PROMPT in prompt

        assert _is_language_prompt_part_contained_in_prompt("C++", prompt)

    def test2(self, flask_test_client):
        flags = PL.NONE
        lang_param = "py"

        flags_param = int(flags)
        response = flask_test_client.get(
            CHAT_ENDPOINT
            + "?flags={}&languages={}".format(flags_param, lang_param)
        )
        flags, prompt = _deconstruct_chat_response(response)

        _print_heading("flags")
        print(flags)
        _print_heading("prompt")
        print(prompt)

        assert flags == PL.py
        assert CHAT_BASIC_PROMPT in prompt

        assert _is_language_prompt_part_contained_in_prompt("Python", prompt)

    # TODO mm languages

    # test languages param  ----------------------------------------------------


# helper  ######################################################################
def _deconstruct_chat_response(response):
    content = response.data.decode("utf-8")
    data = json.loads(content)
    flags = data["flags"]
    prompt = data["prompt"]
    print(prompt)  # HACK
    return flags, prompt


def _is_language_prompt_part_contained_in_prompt(heading, prompt):
    kyc_node = load_embedded_prompt_corpus()["Role"]["Kaye Peer Coder"][
        heading
    ]
    language_prompt = "\n".join(kyc_node._generate_prompt_lines())
    return language_prompt in prompt
