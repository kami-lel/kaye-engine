"""
cli-a-s-prompts-gap_review_test.py

Unit Tests (using pytest) for:

creation of ``gap-review``
"""

import pytest

from tests.cli import *  # noqa: F401, F403
from tests.cli.a.s import (
    VERSION_LINE_PATTERN,
    convert_folder_path2skill_file_path,
)

# constants  ###################################################################


SKILL_NAME = "gap-review"
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
        assert assert_claude_header_line_name(SKILL_NAME, testee_header)

    def test_description(_, testee_header):
        keyword = TESTEE_DESCRIPTION_CONTENT_ALL[SKILL_NAME]
        assert any(keyword in line for line in testee_header)

    def test_version(_, testee_header):
        assert any(VERSION_LINE_PATTERN.match(line) for line in testee_header)


class TestStructure:  # ========================================================

    def test_structure(_, testee_skill_file):
        assert assert_frontmatter_md_file_basic_structure(testee_skill_file)


class TestContent:  # ==========================================================

    @pytest.mark.parametrize("i", range(len(TESTEE_FILE_CONTENT)))
    def test_content(_, testee_content, i):
        assert TESTEE_FILE_CONTENT[i] in testee_content


class TestPrerequisite:  # ====================================================

    def test_heading(_, testee_content):
        assert assert_prerequisite_heading_line(testee_content, 3)

    @pytest.mark.parametrize("i", range(len(TESTEE_PREREQUISITE_CONTENT)))
    def test_prerequisite(_, testee_content, i):
        assert assert_prerequisite_content_line(SKILL_NAME, testee_content, i)
