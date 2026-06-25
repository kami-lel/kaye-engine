"""
cli-a-c-claude_md_test.py

Unit Tests (using pytest) for:

``python -m kaye claude code`` — verifies CLAUDE.md is created in the
exported folder with content equivalent to ``kaye claude u -c``.
"""

import pytest

from tests import (
    TESTEE_INTRODUCTION_CONTENT,
    TESTEE_MARKDOWN_FORMAT_CONTENT,
    TESTEE_CHAT_ADDITIONAL_CONTENT,
    TESTEE_CHAT_COMMENTARY_CASE_CONTENT,
    TESTEE_CODER_CONTENT,
    TESTEE_AGENT_BEHAVIOR_CONTENT,
    TESTEE_TRIAGE_TAG_CONTENT,
)
from tests.cli.a import TESTEE_CLAUDE_BEHAVIOR_CONTENT


# Fixtures  ####################################################################


@pytest.fixture(scope="session")
def claude_md_content(testee_claude_folder):
    with open(testee_claude_folder / "CLAUDE.md") as f:
        return f.read()


# Unit test classes  ###########################################################


class TestBasic:  # ============================================================

    def test_claude_md_exists(self, testee_claude_folder):
        assert (testee_claude_folder / "CLAUDE.md").exists()

    def test_claude_md_is_file(self, testee_claude_folder):
        assert (testee_claude_folder / "CLAUDE.md").is_file()


class TestContent:  # ===========================================================

    @pytest.mark.parametrize("marker", TESTEE_INTRODUCTION_CONTENT)
    def test_introduction(self, claude_md_content, marker):
        assert marker in claude_md_content

    @pytest.mark.parametrize("marker", TESTEE_MARKDOWN_FORMAT_CONTENT)
    def test_markdown_format(self, claude_md_content, marker):
        assert marker in claude_md_content

    @pytest.mark.parametrize("marker", TESTEE_CHAT_ADDITIONAL_CONTENT)
    def test_chat_additional(self, claude_md_content, marker):
        assert marker in claude_md_content

    @pytest.mark.parametrize("marker", TESTEE_CHAT_COMMENTARY_CASE_CONTENT)
    def test_chat_commentary_case(self, claude_md_content, marker):
        assert marker in claude_md_content

    @pytest.mark.parametrize("marker", TESTEE_CODER_CONTENT)
    def test_coder(self, claude_md_content, marker):
        assert marker in claude_md_content

    @pytest.mark.parametrize("marker", TESTEE_TRIAGE_TAG_CONTENT)
    def test_triage_tags(self, claude_md_content, marker):
        assert marker in claude_md_content

    @pytest.mark.parametrize("marker", TESTEE_AGENT_BEHAVIOR_CONTENT)
    def test_agent_behavior(self, claude_md_content, marker):
        assert marker in claude_md_content

    @pytest.mark.parametrize("marker", TESTEE_CLAUDE_BEHAVIOR_CONTENT)
    def test_claude_behavior(self, claude_md_content, marker):
        assert marker in claude_md_content
