"""
cli-a-u-content_test.py

Unit Tests (using pytest) for:

CLAUDE.md content produced by ``kaye claude user-system-prompt`` for each
flag combination (default, -r, -c, -r -c)
"""

# FIXME difficult to read & understand

import pytest

from tests import (
    TESTEE_INTRODUCTION_CONTENT,
    TESTEE_MARKDOWN_FORMAT_CONTENT,
    TESTEE_CHAT_ADDITIONAL_CONTENT,
    TESTEE_CHAT_COMMENTARY_CASE_CONTENT,
    TESTEE_CODER_CONTENT,
    TESTEE_AGENT_BEHAVIOR_CONTENT,
)
from tests.cli.a import TESTEE_CLAUDE_BEHAVIOR_CONTENT

# stem groups  #################################################################

ALL_STEMS = ["chat", "rapid", "coder", "rapid_coder"]
CHAT_STEMS = ["chat", "coder"]  # chat-based; have persona + commentary
RAPID_STEMS = ["rapid", "rapid_coder"]  # rapid-based; persona/commentary absent
NON_CODER_STEMS = ["chat", "rapid"]  # no Kaye Peer Coder


# Pytest unit tests  ###########################################################


class TestBasic:  # ============================================================

    @pytest.mark.parametrize("stem", ALL_STEMS)
    def test_existence(_, request, stem):
        assert request.getfixturevalue(stem + "_path").exists()

    @pytest.mark.parametrize("stem", ALL_STEMS)
    def test_is_file(_, request, stem):
        assert request.getfixturevalue(stem + "_path").is_file()


class TestIntroductionContent:  # ==============================================

    @pytest.mark.parametrize("stem", ALL_STEMS)
    @pytest.mark.parametrize("marker", TESTEE_INTRODUCTION_CONTENT)
    def test_content(_, request, stem, marker):
        assert marker in request.getfixturevalue(stem + "_content")


class TestMarkdownFormatContent:  # ============================================

    @pytest.mark.parametrize("stem", ALL_STEMS)
    @pytest.mark.parametrize("marker", TESTEE_MARKDOWN_FORMAT_CONTENT)
    def test_content(_, request, stem, marker):
        assert marker in request.getfixturevalue(stem + "_content")


class TestChatAdditionalContent:  # ============================================

    @pytest.mark.parametrize("stem", CHAT_STEMS)
    @pytest.mark.parametrize("marker", TESTEE_CHAT_ADDITIONAL_CONTENT)
    def test_content(_, request, stem, marker):
        assert marker in request.getfixturevalue(stem + "_content")

    @pytest.mark.parametrize("stem", RAPID_STEMS)
    @pytest.mark.parametrize("marker", TESTEE_CHAT_ADDITIONAL_CONTENT)
    def test_absent(_, request, stem, marker):
        assert marker not in request.getfixturevalue(stem + "_content")


class TestChatCommentaryCaseContent:  # ========================================

    @pytest.mark.parametrize("stem", CHAT_STEMS)
    @pytest.mark.parametrize("marker", TESTEE_CHAT_COMMENTARY_CASE_CONTENT)
    def test_content(_, request, stem, marker):
        assert marker in request.getfixturevalue(stem + "_content")

    @pytest.mark.parametrize("stem", RAPID_STEMS)
    @pytest.mark.parametrize("marker", TESTEE_CHAT_COMMENTARY_CASE_CONTENT)
    def test_absent(_, request, stem, marker):
        assert marker not in request.getfixturevalue(stem + "_content")


class TestCoderContent:  # ====================================================

    @pytest.mark.parametrize("stem", ["coder", "rapid_coder"])
    @pytest.mark.parametrize("marker", TESTEE_CODER_CONTENT)
    def test_content(_, request, stem, marker):
        assert marker in request.getfixturevalue(stem + "_content")

    @pytest.mark.parametrize("stem", NON_CODER_STEMS)
    @pytest.mark.parametrize("marker", TESTEE_CODER_CONTENT)
    def test_absent(_, request, stem, marker):
        assert marker not in request.getfixturevalue(stem + "_content")


class TestAgentBehaviorContent:  # ==============================================

    @pytest.mark.parametrize("stem", ALL_STEMS)
    @pytest.mark.parametrize("marker", TESTEE_AGENT_BEHAVIOR_CONTENT)
    def test_content(_, request, stem, marker):
        assert marker in request.getfixturevalue(stem + "_content")


class TestClaudeBehaviorContent:  # =============================================

    @pytest.mark.parametrize("stem", ALL_STEMS)
    @pytest.mark.parametrize("marker", TESTEE_CLAUDE_BEHAVIOR_CONTENT)
    def test_content(_, request, stem, marker):
        assert marker in request.getfixturevalue(stem + "_content")
