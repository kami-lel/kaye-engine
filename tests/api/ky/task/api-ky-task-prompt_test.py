"""
api-ky-task-prompt_test.py

Unit Tests (using pytest) for:

/kaye/dify-api/ky/task with role=prompt
"""

import pytest


from tests import TESTEE_FILE_CONTENT_ALL
from tests.api.ky.task import *

# constants  ###################################################################


TESTEE_FILE_CONTENT = TESTEE_FILE_CONTENT_ALL["prompt-writer"]

# pytest fixtures  #############################################################


@pytest.fixture(scope="class")
def opt(flask_test_client, task_endpoint):
    role = "prompt"
    return create_opt_from_role(flask_test_client, task_endpoint, role)


# Pytest unit tests  ###########################################################


class TestP:  # ================================================================

    @pytest.mark.parametrize("i", range(len(TESTEE_FILE_CONTENT)))
    def test_content(_, opt, i):
        assert TESTEE_FILE_CONTENT[i] in opt

    # rapid blueprint  *********************************************************

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
