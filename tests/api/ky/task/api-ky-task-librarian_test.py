"""
api-ky-task-librarian_test.py

Unit Tests (using pytest) for:

/kaye/dify-api/ky/task with role=librarian
"""

import json


import pytest


from tests.api.ky.task import *

# pytest fixtures  #############################################################


@pytest.fixture(scope="class")
def opt(flask_test_client, task_endpoint):
    role = "librarian"

    response = flask_test_client.post(
        task_endpoint,
        data=json.dumps({"role": role}),
        content_type="application/json",
    )

    opt = response.get_data().decode("utf-8")

    return opt


# Pytest unit tests  ###########################################################


class TestLib:  # ==============================================================

    def test_lib00(_, opt):
        assert "## Librarian" in opt

    def test_lib01(_, opt):
        assert "As a *librarian role*" in opt

    def test_lib11(_, opt):
        assert "#### Reading Notes Guidelines" in opt

    def test_lib12(_, opt):
        assert "- **For Each Paragraph:**" in opt

    def test_lib13(_, opt):
        assert "- **Preserve Original Structure" in opt

    def test_lib14(_, opt):
        assert "- Retain the natural progression" in opt

    def test_lib15(_, opt):
        assert "- Refrain from incorporating information" in opt

    def test_lib_bib0(_, opt):
        assert "### Bibliographer" in opt

    def test_lib_bib1(_, opt):
        assert "you **must** generate a **citation paragraph**" in opt

    def test_lib_bib2(_, opt):
        assert "##### Citation Paragraph Format" in opt

    def test_lib_bib3(_, opt):
        assert "- the citation paragraph contains two parts:" in opt

    def test_lib_bib4(_, opt):
        assert ">Schmemann, Serge. “The Voice of America Falls Silent.”" in opt

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

    def test_element_title(_, opt):
        print(opt)
        assert_element_title(opt)

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
