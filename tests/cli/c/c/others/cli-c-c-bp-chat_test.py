"""
cli-c-c-bp-chat_test.py

Unit Tests (using pytest) for:

creation of ``Chat.md``
"""

import pytest

from tests.cli import MD_FILENAME2SKILL_NAME
from tests.cli import (
    assert_frontmatter_md_file_basic_structure,
    split_frontmatter_md_file,
    assert_header_line_always_apply,
)

# constants  ###################################################################
MD_FILENAME = "chat"
_SKILL_NAME = MD_FILENAME2SKILL_NAME[MD_FILENAME]

# Pytest fixtures  #############################################################


@pytest.fixture(scope="session")
def testee_path(testee_rules_folder):
    return testee_rules_folder / (_SKILL_NAME + ".md")


@pytest.fixture(scope="session")
def testee(testee_path):
    with open(testee_path) as f:
        return f.read()


@pytest.fixture(scope="session")
def testee_header(testee):
    return split_frontmatter_md_file(testee)[0]


@pytest.fixture(scope="session")
def testee_content(testee):
    return split_frontmatter_md_file(testee)[1]


# Pytest unit tests  ###########################################################


class TestBasic:  # ============================================================

    def test_existence(_, testee_path):
        assert testee_path.exists()

    def test_is_file(_, testee_path):
        assert testee_path.is_file()

    def test_structure(_, testee):
        assert assert_frontmatter_md_file_basic_structure(testee)


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
