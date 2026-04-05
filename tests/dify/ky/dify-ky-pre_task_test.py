"""
dify-ky-pre_task_test.py

Unit Tests (using pytest) for:

``pre_task`` node of Kaye Chat Dify App
"""

import json

import pytest


from dify_studio.kaye_chat.nodes import pre_task
from dify_studio.kaye_chat.nodes.pre_task import (
    OUTPUT_BODY_KEY,
    OUTPUT_DIRECT_KEY,
    OUTPUT_LLMS_KEY,
)

# helpers  #####################################################################


def _assert_structure(opt):
    assert OUTPUT_BODY_KEY in opt
    assert isinstance(opt[OUTPUT_BODY_KEY], str)
    assert OUTPUT_LLMS_KEY in opt
    assert isinstance(opt[OUTPUT_LLMS_KEY], list)
    assert all(isinstance(e, str) for e in opt)
    assert OUTPUT_DIRECT_KEY in opt
    assert isinstance(opt[OUTPUT_DIRECT_KEY], bool)


# Pytest fixtures  #############################################################


@pytest.fixture
def kwargs():
    return {
        "query": "",
        "current_role": "",
        "current_pls": "",
        "difficulty": 0.0,
    }


# Pytest unit tests  ###########################################################


class TestBody:  # =============================================================

    def test1(_, kwargs):
        kwargs["query"] = "AABBCC"
        kwargs["current_role"] = "chat"
        kwargs["current_pls"] = "cpp,py"

        opt = pre_task.main(**kwargs)

        print(opt)

        _assert_structure(opt)

        body = json.loads(opt[OUTPUT_BODY_KEY])
        assert body == {
            "query": "AABBCC",
            "role": "chat",
            "programming_languages": "cpp,py",
        }

    def test2(_, kwargs):
        kwargs["query"] = "AABBCC"
        kwargs["current_role"] = "chat"
        kwargs["current_pls"] = ""

        opt = pre_task.main(**kwargs)

        print(opt)

        _assert_structure(opt)

        body = json.loads(opt[OUTPUT_BODY_KEY])
        assert body == {
            "query": "AABBCC",
            "role": "chat",
            "programming_languages": "",
        }


class TestLLM:  # ==============================================================

    def test1(_, kwargs):
        kwargs["difficulty"] = 0.01

        opt = pre_task.main(**kwargs)
        print(opt)

        llms = opt[OUTPUT_LLMS_KEY]
        direct = opt[OUTPUT_DIRECT_KEY]

        assert llms == ["gpt-5-nano"]
        assert direct

    def test2(_, kwargs):
        kwargs["difficulty"] = 0.21

        opt = pre_task.main(**kwargs)
        print(opt)

        llms = opt[OUTPUT_LLMS_KEY]
        direct = opt[OUTPUT_DIRECT_KEY]

        assert llms == ["claude-sonnet-4.6"]
        assert direct

    def test3(_, kwargs):
        kwargs["difficulty"] = 0.65

        opt = pre_task.main(**kwargs)
        print(opt)

        llms = opt[OUTPUT_LLMS_KEY]
        direct = opt[OUTPUT_DIRECT_KEY]

        assert llms == ["claude-sonnet-4.6", "gpt-5-mini"]
        assert not direct

    def test4(_, kwargs):
        kwargs["difficulty"] = 0.99

        opt = pre_task.main(**kwargs)
        print(opt)

        llms = opt[OUTPUT_LLMS_KEY]
        direct = opt[OUTPUT_DIRECT_KEY]

        assert llms == ["claude-opus-4.6", "gpt-5"]
        assert not direct
