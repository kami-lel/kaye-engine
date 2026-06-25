"""
api-ky-task-coder-ue.py

Unit Tests (using pytest) for:

/kaye/dify-api/ky/task with:

- role=coder
- PLs=ue
"""

import json


import pytest
from tests import TESTEE_TRIAGE_TAG_CONTENT

from tests.api.ky.task import *
from tests.api.ky.task.coder import *

# pytest fixtures  #############################################################


@pytest.fixture(scope="module")
def opt(flask_test_client, task_endpoint):
    payload = {"role": "coder", "programming_languages": "ue"}

    response = flask_test_client.post(
        task_endpoint,
        data=json.dumps(payload),
        content_type="application/json",
    )

    opt = response.get_data().decode("utf-8")

    return opt





# TT (Triage Tags)  #############################################################


class TestTriageTags:  # ========================================================

    @pytest.mark.parametrize("i", range(len(TESTEE_TRIAGE_TAG_CONTENT)))
    def test_tt_content(_, opt, i):
        assert TESTEE_TRIAGE_TAG_CONTENT[i] in opt
# Pytest unit tests  ###########################################################


class TestCoder:  # ============================================================

    def test_ue0(_, opt):
        assert "## Coder Unreal Engine" in opt

    def test_ue1(_, opt):
        assert "- Version: Unreal Engine `5.6.0`" in opt

    # C++  *********************************************************************

    def test_cpp0(_, opt):
        assert_coder_cpp_title(opt)

    def test_cpp1(_, opt):
        assert_coder_cpp1(opt)

    # C  ***********************************************************************

    def test_c0(_, opt):
        assert_coder_c_title(opt)

    def test_c1(_, opt):
        assert_coder_c1(opt)

    # braces  ******************************************************************

    def test_brace_title(_, opt):
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
        assert_tt_title(opt)

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

    def test_role(_, opt):
        print(opt)
        assert_role(opt)
