"""
api-ky-task-prompt_test.py

Unit Tests (using pytest) for:

/kaye/dify-api/ky/task with role=prompt
"""

import json


import pytest


from tests.api.ky.task import *

# pytest fixtures  #############################################################


@pytest.fixture(scope="class")
def opt(flask_test_client, task_endpoint):
    payload_json_dumps = json.dumps({"role": "prompt"})

    response = flask_test_client.post(
        task_endpoint,
        data=payload_json_dumps,
        content_type="application/json",
    )

    opt = response.get_data().decode("utf-8")

    return opt


# Pytest unit tests  ###########################################################


class TestP:  # ================================================================

    def test0(_, opt):
        assert "## Prompt Writer" in opt

    def test1(_, opt):
        assert "You perform *prompt writer role*" in opt

    def test2(_, opt):
        assert "- write a comprehensive and complete *prompt*" in opt

    def test3(_, opt):
        assert "- fix grammar and spelling errors in the *prompt*" in opt

    def test4(_, opt):
        assert "- strictly follow the syntax and format of" in opt

    # rapid blueprint  *********************************************************

    def test_intro1(_, opt):
        assert_intro1(opt)

    def test_intro2(_, opt):
        assert_intro2(opt)

    def test_format_title(_, opt):
        assert_format_title(opt)

    def test_format1(_, opt):
        assert_format1(opt)

    def test_format2(_, opt):
        assert_format2(opt)

    def test_format3(_, opt):
        assert_format3(opt)

    def test_format4(_, opt):
        assert_format4(opt)

    def test_format5(_, opt):
        assert_format5(opt)

    def test_format_list1(_, opt):
        assert_format_list1(opt)

    def test_format_list2(_, opt):
        assert_format_list2(opt)

    def test_format_list3(_, opt):
        assert_format_list3(opt)

    def test_format_math1(_, opt):
        assert_format_math1(opt)

    def test_format_math2(_, opt):
        assert_format_math2(opt)

    def test_format_math3(_, opt):
        assert_format_math3(opt)

    def test_format_diagrams1(_, opt):
        assert_format_diagrams1(opt)

    def test_format_diagrams2(_, opt):
        assert_format_diagrams2(opt)

    def test_format_diagrams3(_, opt):
        assert_format_diagrams3(opt)

    # abbr *********************************************************************

    def test_abbr_heading(_, opt):
        assert_abbr_heading(opt)
