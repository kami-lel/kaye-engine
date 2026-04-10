"""
dify-ky-pre_sense_test.py

Unit Tests (using pytest) for:

``pre_sense`` node of Kaye Chat Dify App
"""

import json


import pytest


from dify_studio.kaye_chat.nodes.sense import pre_sense
from dify_studio.kaye_chat.nodes.sense.pre_sense import (
    OUTPUT_BODY_KEY,
    OUTPUT_QUERY_KEY,
)

# helpers  #####################################################################


def _assert_structure(opt):
    assert OUTPUT_BODY_KEY in opt
    assert isinstance(opt[OUTPUT_BODY_KEY], str)
    assert OUTPUT_QUERY_KEY in opt
    assert isinstance(opt[OUTPUT_QUERY_KEY], str)


# Pytest fixtures  #############################################################
@pytest.fixture
def kwargs():
    return {"current_role": "", "difficulty_override": 0, "query": ""}


# Pytest unit tests  ###########################################################


class TestBody:  # =============================================================

    def test1(_, kwargs):
        opt = pre_sense.main(**kwargs)
        _assert_structure(opt)
        print(opt)

        body = json.loads(opt[OUTPUT_BODY_KEY])
        print(body)

        assert body == {"pre_sense_role": "", "difficulty_override": 0}

    def test2(_, kwargs):
        kwargs["difficulty_override"] = 50

        opt = pre_sense.main(**kwargs)
        _assert_structure(opt)
        print(opt)

        body = json.loads(opt[OUTPUT_BODY_KEY])
        print(body)

        assert body == {"pre_sense_role": "", "difficulty_override": 50}

    def test3(_, kwargs):
        kwargs["current_role"] = "coder"

        opt = pre_sense.main(**kwargs)
        _assert_structure(opt)
        print(opt)

        body = json.loads(opt[OUTPUT_BODY_KEY])
        print(body)

        assert body == {"pre_sense_role": "coder", "difficulty_override": 0}


# TODO unit test for pre_sense
