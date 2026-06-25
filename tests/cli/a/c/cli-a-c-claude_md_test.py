"""
cli-a-c-claude_md_test.py

Unit Tests (using pytest) for:

``python -m kaye claude code`` — verifies CLAUDE.md is created in the
exported folder with content equivalent to ``kaye claude u -c``.
"""

import pytest

from tests.cli.a.u import (
    TESTEE_INTRODUCTION_CONTENT,
    TESTEE_MARKDOWN_FORMAT_CONTENT,
    TESTEE_CHAT_ADDITIONAL_CONTENT,
    TESTEE_CHAT_COMMENTARY_CASE_CONTENT,
    TESTEE_CODER_CONTENT,
)


# Unit test classes  ###########################################################


class TestBasic:  # ============================================================

    def test_claude_md_exists(self, testee_claude_folder):
        assert (testee_claude_folder / "CLAUDE.md").exists()

    def test_claude_md_is_file(self, testee_claude_folder):
        assert (testee_claude_folder / "CLAUDE.md").is_file()


class TestIntroductionContent:  # ==============================================

    @pytest.fixture(scope="class")
    def claude_md_content(self, testee_claude_folder):
        with open(testee_claude_folder / "CLAUDE.md") as f:
            return f.read()

    @pytest.mark.parametrize("marker", TESTEE_INTRODUCTION_CONTENT)
    def test_content(self, claude_md_content, marker):
        assert marker in claude_md_content


class TestMarkdownFormatContent:  # ============================================

    @pytest.fixture(scope="class")
    def claude_md_content(self, testee_claude_folder):
        with open(testee_claude_folder / "CLAUDE.md") as f:
            return f.read()

    @pytest.mark.parametrize("marker", TESTEE_MARKDOWN_FORMAT_CONTENT)
    def test_content(self, claude_md_content, marker):
        assert marker in claude_md_content


class TestChatAdditionalContent:  # ============================================

    @pytest.fixture(scope="class")
    def claude_md_content(self, testee_claude_folder):
        with open(testee_claude_folder / "CLAUDE.md") as f:
            return f.read()

    @pytest.mark.parametrize("marker", TESTEE_CHAT_ADDITIONAL_CONTENT)
    def test_content(self, claude_md_content, marker):
        assert marker in claude_md_content


class TestChatCommentaryCaseContent:  # ========================================

    @pytest.fixture(scope="class")
    def claude_md_content(self, testee_claude_folder):
        with open(testee_claude_folder / "CLAUDE.md") as f:
            return f.read()

    @pytest.mark.parametrize("marker", TESTEE_CHAT_COMMENTARY_CASE_CONTENT)
    def test_content(self, claude_md_content, marker):
        assert marker in claude_md_content


class TestCoderContent:  # ======================================================

    @pytest.fixture(scope="class")
    def claude_md_content(self, testee_claude_folder):
        with open(testee_claude_folder / "CLAUDE.md") as f:
            return f.read()

    @pytest.mark.parametrize("marker", TESTEE_CODER_CONTENT)
    def test_content(self, claude_md_content, marker):
        assert marker in claude_md_content
