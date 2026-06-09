"""
cli-ce-c-blueprint-chat_test.py

Unit Tests (using pytest) for:

creation of ``Chat.md``
"""

import pytest

from tests.cli.ce.c import (
    assert_rule_file_basic_format,
    split_rule_file_basic_format,
    assert_header_line_always_apply,
)

# Pytest fixtures  #############################################################


@pytest.fixture(scope="session")
def testee(testee_rules_folder):
    with open(testee_rules_folder / "Chat.md") as f:
        return f.read()


@pytest.fixture(scope="session")
def testee_header(testee):
    return split_rule_file_basic_format(testee)[0]


@pytest.fixture(scope="session")
def testee_content(testee):
    return split_rule_file_basic_format(testee)[1]


# Pytest unit tests  ###########################################################


class TestStructure:  # ========================================================

    def test_structure(_, testee):
        assert assert_rule_file_basic_format(testee)


class TestHeader:  # ===========================================================

    def test_name(_, testee_header):
        assert "name: Chat" in testee_header

    def test_description(_, testee_header):
        assert (
            "description: default for general conversation with full"
            " Kaye persona and role"
            in testee_header
        )

    def test_always_apply(_, testee_header):
        assert_header_line_always_apply(testee_header, True)


class TestContent:  # ==========================================================

    def test_introduction_heading(_, testee_content):
        assert "# Introduction" in testee_content

    def test_personality_heading(_, testee_content):
        assert "# Personality" in testee_content

    def test_format_heading(_, testee_content):
        assert "# Format" in testee_content

    def test_language_heading(_, testee_content):
        assert "# Language" in testee_content

    def test_role_heading(_, testee_content):
        assert "# Role" in testee_content

    def test_list_format_heading(_, testee_content):
        assert "### List Format" in testee_content

    def test_math_formatting_heading(_, testee_content):
        assert "### Math Formatting" in testee_content

    def test_diagrams_heading(_, testee_content):
        assert "### Diagrams" in testee_content

    def test_blockquote_emotion_rule(_, testee_content):
        assert "- must use blockquote `>` for your emotions" in testee_content

    def test_language_consistency(_, testee_content):
        assert "- always respond in the **same language**" in testee_content
