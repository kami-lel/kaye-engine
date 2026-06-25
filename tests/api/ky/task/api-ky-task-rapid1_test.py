"""
api-ky-task-rapid1_test.py

Unit Tests (using pytest) for:

/kaye/dify-api/ky/task with:

- role=rapid
- PLs not provided
"""

import pytest

from tests.api.ky.task import (
    TESTEE_INTRODUCTION_CONTENT,
    TESTEE_MARKDOWN_FORMAT_CONTENT,
    create_opt_from_role,
)

# Pytest fixtures  #############################################################


@pytest.fixture(scope="class")
def opt(flask_test_client, task_endpoint):
    role = "rapid"
    return create_opt_from_role(flask_test_client, task_endpoint, role)


# Pytest unit tests  ###########################################################


class TestIntroductionContent:  # ==============================================

    @pytest.mark.parametrize("marker", TESTEE_INTRODUCTION_CONTENT)
    def test_content(_, opt, marker):
        assert marker in opt


class TestMarkdownFormatContent:  # ============================================

    @pytest.mark.parametrize("marker", TESTEE_MARKDOWN_FORMAT_CONTENT)
    def test_content(_, opt, marker):
        assert marker in opt


class TestAbbreviations:  # ==============================================

    def test_abbr_heading(_, opt):
        assert "# (Abbreviations)" in opt
