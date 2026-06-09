"""
api-ky-task-changelog_test.py

Unit Tests (using pytest) for:

/kaye/dify-api/ky/task with role=changelog
"""

import pytest


from tests.api.ky.task import *

# pytest fixtures  #############################################################


@pytest.fixture(scope="class")
def opt(flask_test_client, task_endpoint):
    role = "changelog"
    return create_opt_from_role(flask_test_client, task_endpoint, role)


# Pytest unit tests  ###########################################################


class TestCL:  # ===============================================================

    def test0(_, opt):
        assert "## Coder CHANGELOG Writer" in opt

    def test1(_, opt):
        assert "You must help user to write CHANGELOG." in opt

    def test2(_, opt):
        assert "- changelogs are *for humans*, not machines" in opt

    def test3(_, opt):
        assert "- the latest version comes first" in opt

    def test4(_, opt):
        assert "- `Added`: new features" in opt

    def test5(_, opt):
        assert "- `Fixed`: any bug fixes" in opt

    def test6(_, opt):
        assert "# Example Project CHANGELOG" in opt

    def test7(_, opt):
        assert (
            "[2.0.0]: https://github.com/example-user/"
            "example-project/releases/tag/v2.0.0"
            in opt
        )

    # chat blueprint  **********************************************************

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

    def test_personality_title(_, opt):
        assert_personality_title(opt)

    def test_personality01(_, opt):
        assert_personality01(opt)

    def test_personality02(_, opt):
        assert_personality02(opt)

    def test_personality03(_, opt):
        assert_personality03(opt)

    def test_personality11(_, opt):
        assert_personality11(opt)

    def test_personality12(_, opt):
        assert_personality12(opt)

    def test_personality21(_, opt):
        assert_personality21(opt)

    def test_personality22(_, opt):
        assert_personality22(opt)

    def test_personality23(_, opt):
        assert_personality23(opt)

    def test_personality31(_, opt):
        assert_personality31(opt)

    def test_personality32(_, opt):
        assert_personality32(opt)

    def test_personality33(_, opt):
        assert_personality33(opt)

    def test_lang_title(_, opt):
        assert_lang_title(opt)

    def test_lang1(_, opt):
        assert_lang1(opt)

    def test_lang2(_, opt):
        assert_lang2(opt)

    def test_element11(_, opt):
        assert_element11(opt)

    def test_element12(_, opt):
        assert_element12(opt)

    def test_element13(_, opt):
        assert_element13(opt)

    def test_element21(_, opt):
        assert_element21(opt)

    def test_element22(_, opt):
        assert_element22(opt)

    def test_element23(_, opt):
        assert_element23(opt)

    def test_role(_, opt):
        assert_role(opt)

    # abbr *********************************************************************

    def test_abbr_heading(_, opt):
        assert_abbr_heading(opt)
