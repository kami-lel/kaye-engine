"""
api-ky-task-coder-py.py

Unit Tests (using pytest) for:

/kaye/dify-api/ky/task with:

- role=coder
- PLs=py
"""

import json


import pytest
from tests import (
    TESTEE_TRIAGE_TAG_CONTENT,
    TESTEE_TITLE_CASE_CONTENT,
    TESTEE_CHAT_COMMENTARY_CASE_CONTENT,
    TESTEE_BRIEFNESS_CONTENT,
    TESTEE_STYLE_GUIDE_GOOD_WRITING_CONTENT,
    TESTEE_CODER_CONTENT,
)

from tests.api.ky.task import *
from tests.api.ky.task.coder import *

# pytest fixtures  #############################################################


@pytest.fixture(scope="module")
def opt(flask_test_client, task_endpoint):
    payload = {"role": "coder", "programming_languages": "py"}

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

    def test_py_title(_, opt):
        assert_py_title(opt)

    def test_py_intro(_, opt):
        assert_py_intro(opt)

    def test_py_doc0(_, opt):
        assert_py_doc0(opt)

    def test_py_doc1(_, opt):
        assert_py_doc1(opt)

    def test_py_pytest0(_, opt):
        print(opt)
        assert_py_pytest0(opt)

    def test_py_pytest1(_, opt):
        print(opt)
        assert_py_pytest1(opt)

    def test_py_pytest2(_, opt):
        print(opt)
        assert_py_pytest2(opt)

    # coder shared  ************************************************************

    @pytest.mark.parametrize("marker", TESTEE_CODER_CONTENT)
    def test_coder_content(_, opt, marker):
        assert marker in opt

    @pytest.mark.parametrize("marker", TESTEE_TITLE_CASE_CONTENT)
    def test_style_title_case(_, opt, marker):
        assert marker in opt

    @pytest.mark.parametrize("marker", TESTEE_CHAT_COMMENTARY_CASE_CONTENT)
    def test_style_commentary_case(_, opt, marker):
        assert marker in opt

    @pytest.mark.parametrize("marker", TESTEE_BRIEFNESS_CONTENT)
    def test_style_briefness(_, opt, marker):
        assert marker in opt

    @pytest.mark.parametrize("marker", TESTEE_STYLE_GUIDE_GOOD_WRITING_CONTENT)
    def test_style_good_writing(_, opt, marker):
        assert marker in opt


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
