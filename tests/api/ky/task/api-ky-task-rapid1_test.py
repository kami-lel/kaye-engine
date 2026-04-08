"""
api-ky-task-rapid1_test.py

Unit Tests (using pytest) for:

/kaye/dify-api/ky/task with:

- role=rapid
- PLs not provided
"""

import json

import pytest


from tests.api.ky.task import (
    assert_intro1,
    assert_intro2,
    assert_format_title,
    assert_format1,
    assert_format2,
    assert_format3,
    assert_format4,
    assert_format5,
    assert_format_list1,
    assert_format_list2,
    assert_format_list3,
    assert_format_math1,
    assert_format_math2,
    assert_format_math3,
    assert_format_diagrams1,
    assert_format_diagrams2,
    assert_format_diagrams3,
)

# Pytest fixtures  #############################################################


@pytest.fixture(scope="class")
def opt(flask_test_client, task_endpoint):
    payload = json.dumps({"role": "rapid"})

    response = flask_test_client.post(
        task_endpoint,
        data=payload,
        content_type="application/json",
    )

    return response.get_data().decode("utf-8")


# Pytest unit tests  ###########################################################


class TestNoPls:  # ============================================================

    def test_intro1(_, opt):
        print(opt)
        assert_intro1(opt)

    def test_intro2(_, opt):
        print(opt)
        assert_intro2(opt)

    def test_format_title(_, opt):
        print(opt)
        assert_format_title(opt)

    def test_format1(_, opt):
        print(opt)
        assert_format1(opt)

    def test_format2(_, opt):
        print(opt)
        assert_format2(opt)

    def test_format3(_, opt):
        print(opt)
        assert_format3(opt)

    def test_format4(_, opt):
        print(opt)
        assert_format4(opt)

    def test_format5(_, opt):
        print(opt)
        assert_format5(opt)

    def test_format_list1(_, opt):
        print(opt)
        assert_format_list1(opt)

    def test_format_list2(_, opt):
        print(opt)
        assert_format_list2(opt)

    def test_format_list3(_, opt):
        print(opt)
        assert_format_list3(opt)

    def test_format_math1(_, opt):
        print(opt)
        assert_format_math1(opt)

    def test_format_math2(_, opt):
        print(opt)
        assert_format_math2(opt)

    def test_format_math3(_, opt):
        print(opt)
        assert_format_math3(opt)

    def test_format_diagrams1(_, opt):
        print(opt)
        assert_format_diagrams1(opt)

    def test_format_diagrams2(_, opt):
        print(opt)
        assert_format_diagrams2(opt)

    def test_format_diagrams3(_, opt):
        print(opt)
        assert_format_diagrams3(opt)
