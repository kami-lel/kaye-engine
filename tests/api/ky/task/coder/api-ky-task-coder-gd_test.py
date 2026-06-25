"""
api-ky-task-coder-gd.py

Unit Tests (using pytest) for:

/kaye/dify-api/ky/task with:

- role=coder
- PLs=gdscript;
"""

import json


import pytest
from tests import TESTEE_TRIAGE_TAG_CONTENT

from tests.api.ky.task import *
from tests.api.ky.task.coder import *

# pytest fixtures  #############################################################


@pytest.fixture(scope="module")
def opt(flask_test_client, task_endpoint):
    payload = {"role": "coder", "programming_languages": "gdscript"}

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

    def test0(_, opt):
        assert "## Coder GDScript" in opt

    def test1(_, opt):
        assert "- Version: Godot 4" in opt

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
