"""
cli-s-u-style-gw_test.py

Unit Tests (using pytest) for:

creation of ``style-guide-good-writing``
"""

import pytest

from tests.cli import (
    TESTEE_FILE_CONTENT_ALL,
    assert_frontmatter_md_file_basic_structure,
    split_frontmatter_md_file,
)
from tests.cli.s import (
    VERSION_LINE_PATTERN,
    convert_folder_path2skill_file_path,
)

# constants  ###################################################################


SKILL_NAME = "style-guide-good-writing"
TESTEE_FILE_CONTENT = TESTEE_FILE_CONTENT_ALL[SKILL_NAME]


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
        assert "name: style-guide-good-writing" in testee_header

    def test_description(_, testee_header):
        print(testee_header)
        assert (
            'description: "Proofreads and polishes text with minimal edits'
            " \\u2014 fixing spelling, grammar, punctuation, and clarity while"
            ' preserving the original meaning, voice, and wording."'
            in testee_header
        )

    def test_when(_, testee_header):
        assert (
            "when_to_use: Use to proofread, copyedit, or correct writing"
            " without rewriting. Not for heavy rewrites, summarizing, or tone"
            " changes."
            in testee_header
        )

    def test_version(self, testee_header):
        assert any(VERSION_LINE_PATTERN.match(line) for line in testee_header)


class TestStructure:  # ========================================================

    def test_structure(_, testee_skill_file):
        assert assert_frontmatter_md_file_basic_structure(testee_skill_file)


class TestContent:  # =========================================================

    def test0(_, testee_content):
        assert TESTEE_FILE_CONTENT[0] in testee_content