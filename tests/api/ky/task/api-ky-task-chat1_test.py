"""
api-ky-task-chat1_test.py

Unit Tests (using pytest) for:

/kaye/dify-api/ky/task with:

- role=chat
- no PLs
"""

import pytest

from tests.api.ky.task import (
    TESTEE_INTRODUCTION_CONTENT,
    TESTEE_MD_BASIC_FORMAT_CONTENT,
    TESTEE_MD_ADD_FORMAT_CONTENT,
    TESTEE_CHAT_ADDITIONAL_CONTENT,
    create_opt_from_role,
)

# Pytest fixtures  #############################################################


@pytest.fixture(scope="class")
def opt(flask_test_client, task_endpoint):
    role = "chat"
    return create_opt_from_role(flask_test_client, task_endpoint, role)


# Pytest unit tests  ###########################################################


class TestIntroductionContent:  # ==============================================

    @pytest.mark.parametrize("marker", TESTEE_INTRODUCTION_CONTENT)
    def test_content(_, opt, marker):
        assert marker in opt


class TestMdBasicFormatContent:  # ============================================

    @pytest.mark.parametrize("marker", TESTEE_MD_BASIC_FORMAT_CONTENT)
    def test_content(_, opt, marker):
        assert marker in opt


class TestMdAddFormatContent:  # ==============================================

    @pytest.mark.parametrize("marker", TESTEE_MD_ADD_FORMAT_CONTENT)
    def test_content(_, opt, marker):
        assert marker in opt


class TestChatAdditionalContent:  # ============================================

    @pytest.mark.parametrize("marker", TESTEE_CHAT_ADDITIONAL_CONTENT)
    def test_content(_, opt, marker):
        assert marker in opt


class TestRoleAndElements:  # ====================================================

    def test_role(_, opt):
        assert "# Role" in opt

    def test_abbr_heading(_, opt):
        assert "# (Abbreviations)" in opt
