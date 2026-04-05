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
def default_kwargs():
    return {
        "query": "",
        "current_role": "",
        "current_pls": "",
        "difficulty": 0.0,
    }


# Pytest unit tests  ###########################################################


class TestBody:  # =============================================================

    def test1(_, default_kwargs):
        default_kwargs["query"] = "AABBCC"
        default_kwargs["current_role"] = "chat"
        default_kwargs["current_pls"] = "cpp,py"

        opt = pre_task.main(**default_kwargs)

        print(opt)

        _assert_structure(opt)

        body = json.loads(opt[OUTPUT_BODY_KEY])
        assert body == {
            "query": "AABBCC",
            "role": "chat",
            "programming_languages": "cpp,py",
        }

    def test2(_, default_kwargs):
        default_kwargs["query"] = "AABBCC"
        default_kwargs["current_role"] = "chat"
        default_kwargs["current_pls"] = ""

        opt = pre_task.main(**default_kwargs)

        print(opt)

        _assert_structure(opt)

        body = json.loads(opt[OUTPUT_BODY_KEY])
        assert body == {
            "query": "AABBCC",
            "role": "chat",
            "programming_languages": "",
        }


class TestLLM:

    def test1(_):
        pass  # TODO
