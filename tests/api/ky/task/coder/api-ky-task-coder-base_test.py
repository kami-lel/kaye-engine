"""
api-ky-task-coder-base_test.py

Unit Tests (using pytest) for:

/kaye/dify-api/ky/task with role=coder
"""

import json


import pytest

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

    # coder intro  *************************************************************

    def test_coder_title(_, opt):
        print(opt)
        assert_coder_title(opt)

    def test_coder1(_, opt):
        print(opt)
        assert "Duties are as follows" in opt

    def test_coder2(_, opt):
        print(opt)
        assert "provide code **expansion** per user" in opt

    def test_coder3(_, opt):
        print(opt)
        assert "- offer concise coding **support** with" in opt

    def test_coder4(_, opt):
        print(opt)
        assert "include only minimal explanation" in opt

    # code format  *************************************************************

    def test_coder_code_format_title(_, opt):
        print(opt)
        assert_coder_code_format_title(opt)

    def test_coder_code_format1(_, opt):
        print(opt)
        assert "- each line must not exceed **80 characters**" in opt

    def test_coder_code_format2(_, opt):
        print(opt)
        assert "- when the file name is known," in opt

    def test_coder_code_format3(_, opt):
        print(opt)
        assert "```python utils.py" in opt

    # variable naming  *********************************************************

    def test_coder_variable_naming_title(_, opt):
        print(opt)
        assert_coder_variable_naming_title(opt)

    def test_coder_variable_naming1(_, opt):
        print(opt)
        assert "- use i, j, k for loop counters" in opt

    def test_coder_variable_naming2(_, opt):
        print(opt)
        assert "  `calculate_sum`, `init_graphic_engine`" in opt

    def test_coder_variable_naming3(_, opt):
        print(opt)
        assert "- use UPPER_CASE_WITH_UNDERSCORES for constants" in opt

    # code comment  ************************************************************

    def test_coder_code_comment_title(_, opt):
        print(opt)
        assert_coder_code_comment_title(opt)

    def test_coder_code_comment1(_, opt):
        print(opt)
        assert "- format inline comments as:" in opt

    def test_coder_code_comment2(_, opt):
        print(opt)
        assert "- use *Commentary Case* for each comment line" in opt

    def test_coder_code_comment3(_, opt):
        print(opt)
        assert "- include *immediate annotation markers*" in opt

    # csh  *********************************************************************

    def test_coder_csh_title(_, opt):
        print(opt)
        assert_coder_csh_title(opt)

    def test_coder_csh1(_, opt):
        print(opt)
        assert "**Comment section headings** (CSH) are visual" in opt

    def test_coder_csh2(_, opt):
        print(opt)
        assert "- CSH must live **inside code comments only**" in opt

    def test_coder_csh3(_, opt):
        print(opt)
        assert "- use CSH **sparingly** — prefer blank lines to" in opt

    def test_coder_csh4(_, opt):
        print(opt)
        assert "- symbol order for descending levels:" in opt

    def test_coder_csh5(_, opt):
        print(opt)
        assert "**Examples:**" in opt

    def test_coder_csh6(_, opt):
        print(opt)
        assert "```cpp stats_demo.cpp" in opt

    def test_coder_csh7(_, opt):
        print(opt)
        assert "def to_int(s):" in opt

    # style  *******************************************************************

    def test_style_title(_, opt):
        assert_style_title(opt)

    def test_style_caps(_, opt):
        assert_style_caps(opt)

    def test_style_caps_tc0(_, opt):
        assert_style_caps_tc0(opt)

    def test_style_caps_tc1(_, opt):
        assert_style_caps_tc1(opt)

    def test_style_caps_tc2(_, opt):
        assert_style_caps_tc2(opt)

    def test_style_caps_tc3(_, opt):
        assert_style_caps_tc3(opt)

    def test_style_caps_tc4(_, opt):
        assert_style_caps_tc4(opt)

    def test_style_caps_cc0(_, opt):
        assert_style_caps_cc0(opt)

    def test_style_caps_cc1(_, opt):
        assert_style_caps_cc1(opt)

    def test_style_caps_cc2(_, opt):
        assert_style_caps_cc2(opt)

    def test_style_caps_cc3(_, opt):
        assert_style_caps_cc3(opt)

    def test_style_caps_bs0(_, opt):
        assert_style_caps_bs0(opt)

    def test_style_caps_bs1(_, opt):
        assert_style_caps_bs1(opt)

    def test_style_caps_bs2(_, opt):
        assert_style_caps_bs2(opt)

    def test_style_caps_bs3(_, opt):
        assert_style_caps_bs3(opt)

    def test_style_caps_gw0(_, opt):
        assert_style_caps_gw0(opt)

    def test_style_caps_gw1(_, opt):
        assert_style_caps_gw1(opt)

    def test_style_caps_gw2(_, opt):
        assert_style_caps_gw2(opt)

    def test_style_caps_gw3(_, opt):
        assert_style_caps_gw3(opt)

    # AMs  *********************************************************************

    def test_am_title(_, opt):
        assert_am_title(opt)

    def test_am1(_, opt):
        assert_am1(opt)

    def test_am2(_, opt):
        assert_am2(opt)

    def test_am3(_, opt):
        assert_am3(opt)

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
