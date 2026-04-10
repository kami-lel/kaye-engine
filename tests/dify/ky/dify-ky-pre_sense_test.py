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


class TestTruncQuery:  # =======================================================

    def test1(_, kwargs):
        query = "AAA\n" * 50 + "ZZZ\n" * 51

        kwargs["query"] = query

        opt = pre_sense.main(**kwargs)
        _assert_structure(opt)
        print(opt)

        result = opt[OUTPUT_QUERY_KEY]

        print(result)
        assert query != result

        lines = result.splitlines()
        assert len(lines) == 100
        assert all(v == "AAA" for v in lines[:50])
        assert all(v == "ZZZ" for v in lines[50:])

    def test2(_, kwargs):
        query = "AAA\n" * 65 + "ZZZ\n" * 105

        kwargs["query"] = query

        opt = pre_sense.main(**kwargs)
        _assert_structure(opt)
        print(opt)

        result = opt[OUTPUT_QUERY_KEY]

        print(result)
        assert query != result

        lines = result.splitlines()
        assert len(lines) == 100
        assert all(v == "AAA" for v in lines[:50])
        assert all(v == "ZZZ" for v in lines[50:])

    # no op  -------------------------------------------------------------------

    def test_same1(_, kwargs):
        query = ""

        kwargs["query"] = query

        opt = pre_sense.main(**kwargs)
        _assert_structure(opt)
        print(opt)

        result = opt[OUTPUT_QUERY_KEY]

        print(result)
        assert result == ""

    def test_same2(_, kwargs):
        query = "AAA"

        kwargs["query"] = query

        opt = pre_sense.main(**kwargs)
        _assert_structure(opt)
        print(opt)

        result = opt[OUTPUT_QUERY_KEY]

        print(result)
        assert result == query

    def test_same3(_, kwargs):
        query = "AAA\n" * 20

        kwargs["query"] = query

        opt = pre_sense.main(**kwargs)
        _assert_structure(opt)
        print(opt)

        result = opt[OUTPUT_QUERY_KEY]

        print(result)
        assert result == query

    def test_same4(_, kwargs):
        query = "AAA\n" * 100

        kwargs["query"] = query

        opt = pre_sense.main(**kwargs)
        _assert_structure(opt)
        print(opt)

        result = opt[OUTPUT_QUERY_KEY]

        print(result)
        assert result == query

    def test_same5(_, kwargs):
        query = "AAA\n\n\n" * 100

        kwargs["query"] = query

        opt = pre_sense.main(**kwargs)
        _assert_structure(opt)
        print(opt)

        result = opt[OUTPUT_QUERY_KEY]

        print(result)
        assert result == query
