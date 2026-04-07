"""
dify-ky-pre_task_test.py

Unit Tests (using pytest) for:

``pre_task`` node of Kaye Chat Dify App
"""

import json

import pytest


from dify_studio.kaye_chat.nodes.task import pre_task
from dify_studio.kaye_chat.nodes.task.pre_task import (
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
        "current_difficulty": 0.0,
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
        diff = 0.01
        kwargs["current_difficulty"] = diff

        opt = pre_task.main(**kwargs)
        print(opt)

        llms = opt[OUTPUT_LLMS_KEY]
        direct = opt[OUTPUT_DIRECT_KEY]

        assert llms == ["gpt-4-nano"]
        assert direct

    def test2(_, kwargs):
        diff = 0.05
        kwargs["current_difficulty"] = diff

        opt = pre_task.main(**kwargs)
        print(opt)

        llms = opt[OUTPUT_LLMS_KEY]
        direct = opt[OUTPUT_DIRECT_KEY]

        assert llms == ["gpt-4-nano"]
        assert direct

    def test3(_, kwargs):
        diff = 0.11
        kwargs["current_difficulty"] = diff

        opt = pre_task.main(**kwargs)
        print(opt)

        llms = opt[OUTPUT_LLMS_KEY]
        direct = opt[OUTPUT_DIRECT_KEY]

        assert llms == ["gpt-5-nano"]
        assert direct

    def test4(_, kwargs):
        diff = 0.15
        kwargs["current_difficulty"] = diff

        opt = pre_task.main(**kwargs)
        print(opt)

        llms = opt[OUTPUT_LLMS_KEY]
        direct = opt[OUTPUT_DIRECT_KEY]

        assert llms == ["gpt-5-nano"]
        assert direct

    def test5(_, kwargs):
        diff = 0.21
        kwargs["current_difficulty"] = diff

        opt = pre_task.main(**kwargs)
        print(opt)

        llms = opt[OUTPUT_LLMS_KEY]
        direct = opt[OUTPUT_DIRECT_KEY]

        assert llms == ["gpt-5-nano"]
        assert direct

    def test6(_, kwargs):
        diff = 0.25
        kwargs["current_difficulty"] = diff

        opt = pre_task.main(**kwargs)
        print(opt)

        llms = opt[OUTPUT_LLMS_KEY]
        direct = opt[OUTPUT_DIRECT_KEY]

        assert llms == ["gpt-5-nano"]
        assert direct

    def test7(_, kwargs):
        diff = 0.31
        kwargs["current_difficulty"] = diff

        opt = pre_task.main(**kwargs)
        print(opt)

        llms = opt[OUTPUT_LLMS_KEY]
        direct = opt[OUTPUT_DIRECT_KEY]

        assert llms == ["claude-sonnet-4"]
        assert direct

    def test8(_, kwargs):
        diff = 0.35
        kwargs["current_difficulty"] = diff

        opt = pre_task.main(**kwargs)
        print(opt)

        llms = opt[OUTPUT_LLMS_KEY]
        direct = opt[OUTPUT_DIRECT_KEY]

        assert llms == ["claude-sonnet-4"]
        assert direct

    def test9(_, kwargs):
        diff = 0.41
        kwargs["current_difficulty"] = diff

        opt = pre_task.main(**kwargs)
        print(opt)

        llms = opt[OUTPUT_LLMS_KEY]
        direct = opt[OUTPUT_DIRECT_KEY]

        assert llms == ["claude-sonnet-4"]
        assert direct

    def test10(_, kwargs):
        diff = 0.51
        kwargs["current_difficulty"] = diff

        opt = pre_task.main(**kwargs)
        print(opt)

        llms = opt[OUTPUT_LLMS_KEY]
        direct = opt[OUTPUT_DIRECT_KEY]

        assert llms == ["claude-sonnet-4"]
        assert direct

    def test11(_, kwargs):
        diff = 0.61
        kwargs["current_difficulty"] = diff

        opt = pre_task.main(**kwargs)
        print(opt)

        llms = opt[OUTPUT_LLMS_KEY]
        direct = opt[OUTPUT_DIRECT_KEY]

        assert llms == ["claude-sonnet-4", "gpt-5-mini"]
        assert not direct

    def test12(_, kwargs):
        diff = 0.71
        kwargs["current_difficulty"] = diff

        opt = pre_task.main(**kwargs)
        print(opt)

        llms = opt[OUTPUT_LLMS_KEY]
        direct = opt[OUTPUT_DIRECT_KEY]

        assert llms == ["claude-sonnet-4", "gpt-5-mini"]
        assert not direct

    def test13(_, kwargs):
        diff = 0.81
        kwargs["current_difficulty"] = diff

        opt = pre_task.main(**kwargs)
        print(opt)

        llms = opt[OUTPUT_LLMS_KEY]
        direct = opt[OUTPUT_DIRECT_KEY]

        assert llms == ["claude-sonnet-4", "gpt-5-mini"]
        assert not direct

    def test14(_, kwargs):
        diff = 0.91
        kwargs["current_difficulty"] = diff

        opt = pre_task.main(**kwargs)
        print(opt)

        llms = opt[OUTPUT_LLMS_KEY]
        direct = opt[OUTPUT_DIRECT_KEY]

        assert llms == ["claude-opus-4", "gpt-5", "gemini-3-pro"]
        assert not direct

    def test15(_, kwargs):
        diff = 0.99
        kwargs["current_difficulty"] = diff

        opt = pre_task.main(**kwargs)
        print(opt)

        llms = opt[OUTPUT_LLMS_KEY]
        direct = opt[OUTPUT_DIRECT_KEY]

        assert llms == ["claude-opus-4", "gpt-5", "gemini-3-pro"]
        assert not direct
