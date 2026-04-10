"""
api-ky-task-art_test.py

Unit Tests (using pytest) for:

/kaye/dify-api/ky/task with role=art
"""

import json


import pytest


from tests.api.ky.task import *

# pytest fixtures  #############################################################


@pytest.fixture(scope="class")
def opt(flask_test_client, task_endpoint):
    role = "art"
    return create_role_opt(flask_test_client, task_endpoint, role)


# Pytest unit tests  ###########################################################


class TestArt:  # ==============================================================

    def test_heading(_, opt):

        assert "## Art Tutor" in opt

    def test01(_, opt):
        assert "Your role is to help users craft detailed" in opt

    def test02(_, opt):
        assert "Respond using one of two modes as" in opt

    def test11(_, opt):
        assert "#### A: Information Gathering" in opt

    def test12(_, opt):
        assert "- Guide users through prompt creation" in opt

    def test13(_, opt):
        assert "- Advise on using vivid, precise descriptions" in opt

    def test14(_, opt):
        assert "- Remind users they can request the completed" in opt

    def test21(_, opt):
        assert "#### B: Prompt Generation" in opt

    def test22(_, opt):
        assert "- Use this mode when all required information" in opt

    def test23(_, opt):
        assert "- The prompt must include orientation." in opt

    def test24(_, opt):
        assert "- Conclude with a reminder: Click ⬇️ icon 🖼️" in opt

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
