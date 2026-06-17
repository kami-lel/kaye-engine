"""
cli-a-s-pe-description_test.py

Unit Tests (using pytest) for:

creation of ``skill-description-writer``
"""

import pytest

from tests.cli import (
    TESTEE_FILE_CONTENT_ALL,
    TESTEE_PREREQUISITE_CONTENT_ALL,
    assert_frontmatter_md_file_basic_structure,
    split_frontmatter_md_file,
)
from tests.cli.a.s import (
    VERSION_LINE_PATTERN,
    convert_folder_path2skill_file_path,
)

# constants  ###################################################################


SKILL_NAME = "skill-description-writer"
TESTEE_FILE_CONTENT = TESTEE_FILE_CONTENT_ALL[SKILL_NAME]
TESTEE_PREREQUISITE_CONTENT = TESTEE_PREREQUISITE_CONTENT_ALL[SKILL_NAME]


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
        assert "name: " + SKILL_NAME in testee_header

    def test_version(self, testee_header):
        assert any(VERSION_LINE_PATTERN.match(line) for line in testee_header)


class TestStructure:  # ========================================================

    def test_structure(_, testee_skill_file):
        assert assert_frontmatter_md_file_basic_structure(testee_skill_file)


class TestContent:  # =========================================================

    def test0(_, testee_content):
        assert TESTEE_FILE_CONTENT[0] in testee_content

    def test1(_, testee_content):
        assert TESTEE_FILE_CONTENT[1] in testee_content

    def test2(_, testee_content):
        assert TESTEE_FILE_CONTENT[2] in testee_content

    def test3(_, testee_content):
        assert TESTEE_FILE_CONTENT[3] in testee_content

class TestPrerequisite:  # ====================================================

    def test_heading(_, testee_content):
        assert "### {prerequisite}" in testee_content or "#### {prerequisite}" in testee_content

    def test0(_, testee_content):
        assert TESTEE_PREREQUISITE_CONTENT[0] in testee_content
    def test1(_, testee_content):
        assert TESTEE_PREREQUISITE_CONTENT[1] in testee_content
