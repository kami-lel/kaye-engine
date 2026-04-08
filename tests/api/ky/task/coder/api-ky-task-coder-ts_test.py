"""
api-ky-task-coder-ts.py

Unit Tests (using pytest) for:

/kaye/dify-api/ky/task with:

- role=coder
- PLs=ts
"""

import json


import pytest

from tests.api.ky.task import *
from tests.api.ky.task.coder import *

# pytest fixtures  #############################################################


@pytest.fixture(scope="class")
def opt(flask_test_client, task_endpoint):
    payload = {"role": "coder", "programming_languages": "ts"}

    response = flask_test_client.post(
        task_endpoint,
        data=json.dumps(payload),
        content_type="application/json",
    )

    opt = response.get_data().decode("utf-8")

    return opt


# Pytest unit tests  ###########################################################


class TestCoder:  # ============================================================

    def assert_00(_, opt):
        assert_js_ts00(opt)

    def assert_01(_, opt):
        assert_js_ts01(opt)

    def assert_11(_, opt):
        assert_js_ts11(opt)

    def assert_12(_, opt):
        assert_js_ts12(opt)

    def assert_21(_, opt):
        assert_js_ts21(opt)

    def assert_22(_, opt):
        assert_js_ts22(opt)

    def assert_23(_, opt):
        assert_js_ts23(opt)

    def assert_24(_, opt):
        assert_js_ts24(opt)

    # braces  ******************************************************************

    def assert_brace_title(_, opt):
        assert_brace_title(opt)

    def test_brace1(_, opt):
        assert_brace1(opt)

    def test_brace2(_, opt):
        assert_brace2(opt)

    # coder shared  ************************************************************

    def test_coder_title(_, opt):
        print(opt)
        assert_coder_title(opt)

    def test_coder_code_format_title(_, opt):
        print(opt)
        assert_coder_code_format_title(opt)

    def test_coder_variable_naming_title(_, opt):
        print(opt)
        assert_coder_variable_naming_title(opt)

    def test_coder_code_comment_title(_, opt):
        print(opt)
        assert_coder_code_comment_title(opt)

    def test_coder_csh_title(_, opt):
        print(opt)
        assert_coder_csh_title(opt)

    def test_style_title(_, opt):
        assert_style_title(opt)

    def test_am_title(_, opt):
        assert_am_title(opt)

    # chat blueprint  **********************************************************

    def test_intro1(_, opt):
        print(opt)
        assert_intro1(opt)

    def test_format5(_, opt):
        print(opt)
        assert_format5(opt)

    def test_personality01(_, opt):
        print(opt)
        assert_personality01(opt)

    def test_lang_title(_, opt):
        print(opt)
        assert_lang_title(opt)

    def test_element_title(_, opt):
        print(opt)
        assert_element_title(opt)

    def test_role(_, opt):
        print(opt)
        assert_role(opt)
