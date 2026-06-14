"""
cli-s-u-style-cap_test.py

Unit Tests (using pytest) for:

creation of ``style-guide-capitalization``
"""

import pytest

from tests.cli import (
    assert_frontmatter_md_file_basic_structure,
    split_frontmatter_md_file,
)
from tests.cli.s import convert_folder_path2skill_file_path

# constants  ###################################################################


SKILL_NAME = "style-guide-capitalization"


# Pytest fixtures  #############################################################


@pytest.fixture(scope="session")
def testee_folder(testee_skills_folder):
    return testee_skills_folder / SKILL_NAME


@pytest.fixture(scope="session")
def testee_skill_file_path(testee_folder):
    return convert_folder_path2skill_file_path(testee_folder)


@pytest.fixture(scope="session")
def testee_skill_file(testee_skill_file_path):
    with open(testee_skill_file_path) as f:
        return f.read()


@pytest.fixture(scope="session")
def testee_header(testee_skill_file):
    return split_frontmatter_md_file(testee_skill_file)[0]


@pytest.fixture(scope="session")
def testee_content(testee_skill_file):
    return split_frontmatter_md_file(testee_skill_file)[1]


# Pytest unit tests  ###########################################################


class TestBasic:  # ============================================================

    def test_existence(_, testee_skill_file_path):
        assert testee_skill_file_path.exists()

    def test_is_file(_, testee_skill_file_path):
        assert testee_skill_file_path.is_file()


class TestHeader:  # ===========================================================

    def test_name(_, testee_header):
        assert "name: style-guide-capitalization" in testee_header

    def test_description(_, testee_header):
        print(testee_header)
        assert (
            "description: Applies capitalization rules to text, covering Title"
            " Case (headline-style major-word capitalization for titles and"
            " section headings) and Commentary Case (lowercase-leading"
            " sentences with selective Title Case emphasis and no terminal"
            " punctuation, for list items and table cells)."
            in testee_header
        )

    def test_when(_, testee_header):
        assert (
            "when_to_use: Use when capitalizing or formatting document titles,"
            " section headings, list items, or table cell content, or when a"
            " user mentions title case, headline case, sentence case, Chicago"
            " Manual of Style, or asks how to capitalize headings vs. body/list"
            " text. Triggers on requests to fix, standardize, or check letter"
            " casing in structured documents. Not for grammar, punctuation, or"
            " prose style beyond capitalization."
            in testee_header
        )


class TestStructure:  # ========================================================

    def test_structure(_, testee_skill_file):
        assert assert_frontmatter_md_file_basic_structure(testee_skill_file)


class TestContent:  # ==========================================================

    def test_heading(_, testee_content):
        assert "## Style Guide Capitalization" in testee_content
