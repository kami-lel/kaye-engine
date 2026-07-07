"""
api-ky-task-coder-base_test.py

Unit Tests (using pytest) for:

/kaye/dify-api/ky/task with role=coder
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
    assert_coding_terms_content,
)
from tests.api.ky.task import *
from tests.api.ky.task.coder import *

# pytest fixtures  #############################################################


@pytest.fixture(scope="class")
def opt(flask_test_client, task_endpoint):
    payload = {"role": "coder", "programming_languages": ""}

    response = flask_test_client.post(
        task_endpoint,
        data=json.dumps(payload),
        content_type="application/json",
    )

    opt = response.get_data().decode("utf-8")

    return opt


# Pytest unit tests  ###########################################################


class TestCoder:  # ============================================================

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

    # Triage Tags  *************************************************************

    @pytest.mark.parametrize("i", range(len(TESTEE_TRIAGE_TAG_CONTENT)))
    def test_triage_tags(_, opt, i):
        assert TESTEE_TRIAGE_TAG_CONTENT[i] in opt

    # Coding Terms  ****************************************************************

    def test_coding_terms(_, opt):
        assert_coding_terms_content(opt)

    # chat blueprint  **********************************************************

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

    def test_personality_title(_, opt):
        print(opt)
        assert_personality_title(opt)

    def test_personality01(_, opt):
        print(opt)
        assert_personality01(opt)

    def test_personality02(_, opt):
        print(opt)
        assert_personality02(opt)

    def test_personality03(_, opt):
        print(opt)
        assert_personality03(opt)

    def test_personality11(_, opt):
        print(opt)
        assert_personality11(opt)

    def test_personality12(_, opt):
        print(opt)
        assert_personality12(opt)

    def test_personality21(_, opt):
        print(opt)
        assert_personality21(opt)

    def test_personality22(_, opt):
        print(opt)
        assert_personality22(opt)

    def test_personality23(_, opt):
        print(opt)
        assert_personality23(opt)

    def test_personality31(_, opt):
        print(opt)
        assert_personality31(opt)

    def test_personality32(_, opt):
        print(opt)
        assert_personality32(opt)

    def test_personality33(_, opt):
        print(opt)
        assert_personality33(opt)

    def test_lang_title(_, opt):
        print(opt)
        assert_lang_title(opt)

    def test_lang1(_, opt):
        print(opt)
        assert_lang1(opt)

    def test_lang2(_, opt):
        print(opt)
        assert_lang2(opt)

    def test_element11(_, opt):
        print(opt)
        assert_element11(opt)

    def test_element12(_, opt):
        print(opt)
        assert_element12(opt)

    def test_element13(_, opt):
        print(opt)
        assert_element13(opt)

    def test_element21(_, opt):
        print(opt)
        assert_element21(opt)

    def test_element22(_, opt):
        print(opt)
        assert_element22(opt)

    def test_element23(_, opt):
        print(opt)
        assert_element23(opt)

    def test_role(_, opt):
        print(opt)
        assert_role(opt)

    # abbr *********************************************************************

    def test_abbr_heading(_, opt):
        assert_abbr_heading(opt)
