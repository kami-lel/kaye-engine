"""
cli-c-c-style-cap_test.py

Unit Tests (using pytest) for
"""

import pytest

from tests.cli import MD_FILENAME2SKILL_NAME
from tests.cli import (
    assert_frontmatter_md_file_basic_structure,
    split_frontmatter_md_file,
    assert_header_line_always_apply,
)

# constants  ###################################################################
MD_FILENAME = "style-guide-capitalization"
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
        name_line = "name: " + _SKILL_NAME
        assert name_line in testee_header

    def test_description(_, testee_header):
        print(testee_header)
        assert (
            'description: "Applies capitalization rules to text, covering Title'
            " Case (headline-style major-word capitalization for titles and"
            " section headings) and Commentary Case (lowercase-leading"
            " sentences with selective Title Case emphasis and no terminal"
            " punctuation, for list items and table cells).\\u21B5Use when"
            " capitalizing or formatting document titles, section headings,"
            " list items, or table cell content, or when a user mentions title"
            " case, headline case, sentence case, Chicago Manual of Style, or"
            " asks how to capitalize headings vs. body/list text. Triggers on"
            " requests to fix, standardize, or check letter casing in"
            " structured documents. Not for grammar, punctuation, or prose"
            ' style beyond capitalization."'
            in testee_header
        )

    def test_always_apply(_, testee_header):
        assert_header_line_always_apply(testee_header, False)


class TestContent:  # ==========================================================

    def test_heading(_, testee):
        assert "## Style Guide Capitalization" in testee

    def test_title0(_, testee):
        assert "### Title Case" in testee

    def test_title1(_, testee):
        assert "Use *Chicago Manual of Style* headline case:" in testee

    def test_title2(_, testee):
        assert (
            "- **lowercase minor words**: articles (a, an, the), coordinating"
            " conjunctions (and, but, or, nor, for, so, yet), prepositions (of,"
            " in, on, with, etc.), and the infinitive to"
            in testee
        )

    def test_title3(_, testee):
        assert "Used for **document title** and **section headings**." in testee

    def test_commentary0(_, testee):
        assert "### Commentary Case" in testee

    def test_commentary1(_, testee):
        assert (
            "- begin 1st sentence with a lowercase letter; use standard"
            " sentence capitalization for the 2nd and subsequent sentences"
            in testee
        )

    def test_commentary2(_, testee):
        assert (
            "    # check the Config. Validate the Filepath with the Tool."
            " Process final result"
            in testee
        )

    def test_commentary3(_, testee):
        assert "Used for **list items** and **table cell content**." in testee
