"""
api_dify_kyc_test.py

Unit Tests (using pytest) for: /kaye/dify-app/kyc/*
"""

# Hack deprecations

import json

from kaye.prompt import (
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

        assert _is_language_prompt_part_contained("C++", prompt)

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

        assert _is_language_prompt_part_contained("Python", prompt)

    def test3(self, flask_test_client):
        flags = PL.NONE
        lang_param = "c,cpp,ue"

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

        assert PL.c in flags
        assert PL.cpp in flags
        assert PL.ue in flags

        assert CHAT_BASIC_PROMPT in prompt
        assert _is_language_prompt_part_contained("C", prompt)
        assert _is_language_prompt_part_contained("C++", prompt)
        assert _is_language_prompt_part_contained("Unreal Engine", prompt)

    def test4(self, flask_test_client):
        flags = PL.NONE
        lang_param = "gdscript,html,js,qt"

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

        assert PL.gdscript in flags
        assert PL.html in flags
        assert PL.js in flags
        assert PL.qt in flags

        assert CHAT_BASIC_PROMPT in prompt
        assert _is_language_prompt_part_contained("GDScript", prompt)
        assert _is_language_prompt_part_contained("HTML", prompt)
        assert _is_language_prompt_part_contained(
            "JavaScript & TypeScript", prompt
        )
        assert _is_language_prompt_part_contained("Qt", prompt)

    def test_qml(self, flask_test_client):
        flags = PL.NONE
        lang_param = "qml"

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

        assert PL.qml in flags

        assert CHAT_BASIC_PROMPT in prompt

        node = load_embedded_prompt_corpus()["Role"]["Kaye Peer Coder"]["Qt"][
            "QML"
        ]
        language_prompt = "\n".join(node._generate_prompt_lines())
        assert language_prompt in prompt

    def test_all_one_by_one(_, flask_test_client):
        data = {
            PL.c: "C",
            PL.cpp: "C++",
            PL.ue: "Unreal Engine",
            PL.csharp: "C Sharp",
            PL.u3d: "Unity Engine",
            PL.gdscript: "GDScript",
            PL.html: "HTML",
            PL.js: "JavaScript & TypeScript",
            PL.ts: "JavaScript & TypeScript",
            PL.qt: "Qt",
            PL.py: "Python",
            PL.console: "Message Level",
        }
        for k, v in data.items():
            response = flask_test_client.get(
                CHAT_ENDPOINT + "?flags=0&languages={}".format(k.name)
            )
            flags, prompt = _deconstruct_chat_response(response)

            assert k in flags

            assert CHAT_BASIC_PROMPT in prompt
            assert _is_language_prompt_part_contained(v, prompt)


class TestChatFlags:  # ========================================================

    def test1(self, flask_test_client):
        flags = PL.cpp

        flags_param = int(flags)
        response = flask_test_client.get(
            CHAT_ENDPOINT + "?flags={}".format(flags_param)
        )
        flags, prompt = _deconstruct_chat_response(response)

        _print_heading("flags")
        print(flags)
        _print_heading("prompt")
        print(prompt)

        assert flags == PL.cpp
        assert CHAT_BASIC_PROMPT in prompt
        assert _is_language_prompt_part_contained("C++", prompt)

    def test2(self, flask_test_client):
        flags = PL.html

        flags_param = int(flags)
        response = flask_test_client.get(
            CHAT_ENDPOINT + "?flags={}".format(flags_param)
        )
        flags, prompt = _deconstruct_chat_response(response)

        _print_heading("flags")
        print(flags)
        _print_heading("prompt")
        print(prompt)

        assert flags == PL.html
        assert CHAT_BASIC_PROMPT in prompt
        assert _is_language_prompt_part_contained("HTML", prompt)

    def test3(self, flask_test_client):
        flags = PL.js | PL.u3d

        flags_param = int(flags)
        response = flask_test_client.get(
            CHAT_ENDPOINT + "?flags={}".format(flags_param)
        )
        flags, prompt = _deconstruct_chat_response(response)

        _print_heading("flags")
        print(flags)
        _print_heading("prompt")
        print(prompt)

        assert PL.js in flags
        assert PL.u3d in flags
        assert CHAT_BASIC_PROMPT in prompt
        assert _is_language_prompt_part_contained(
            "JavaScript & TypeScript", prompt
        )
        assert _is_language_prompt_part_contained("Unity Engine", prompt)

    def test4(self, flask_test_client):
        flags = PL.ue | PL.qt | PL.c

        flags_param = int(flags)
        response = flask_test_client.get(
            CHAT_ENDPOINT + "?flags={}".format(flags_param)
        )
        flags, prompt = _deconstruct_chat_response(response)

        _print_heading("flags")
        print(flags)
        _print_heading("prompt")
        print(prompt)

        assert PL.c in flags
        assert PL.ue in flags
        assert PL.qt in flags
        assert CHAT_BASIC_PROMPT in prompt
        assert _is_language_prompt_part_contained("C", prompt)
        assert _is_language_prompt_part_contained("Unreal Engine", prompt)
        assert _is_language_prompt_part_contained("Qt", prompt)


class TestChatBoth:  # =========================================================

    def test1(self, flask_test_client):
        flags = PL.cpp
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

        assert PL.cpp in flags
        assert PL.py in flags
        assert CHAT_BASIC_PROMPT in prompt
        assert _is_language_prompt_part_contained("C++", prompt)
        assert _is_language_prompt_part_contained("Python", prompt)

    def test2(self, flask_test_client):
        flags = PL.c | PL.html
        lang_param = "py,qt,u3d"

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

        assert PL.c in flags
        assert PL.html in flags
        assert PL.py in flags
        assert PL.qt in flags
        assert PL.u3d in flags
        assert CHAT_BASIC_PROMPT in prompt
        assert _is_language_prompt_part_contained("C", prompt)
        assert _is_language_prompt_part_contained("HTML", prompt)
        assert _is_language_prompt_part_contained("Python", prompt)
        assert _is_language_prompt_part_contained("Qt", prompt)
        assert _is_language_prompt_part_contained("Unity Engine", prompt)


# helper  ######################################################################
def _deconstruct_chat_response(response):
    content = response.data.decode("utf-8")
    data = json.loads(content)
    flags = PL(data["flags"])
    prompt = data["prompt"]
    return flags, prompt


def _is_language_prompt_part_contained(heading, prompt):
    kyc_node = load_embedded_prompt_corpus()["Role"]["Kaye Peer Coder"][heading]
    language_prompt = "\n".join(kyc_node._generate_prompt_lines())
    return language_prompt in prompt
