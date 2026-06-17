"""
cli-a-s-proj-agents_test.py

Unit Tests (using pytest) for:

creation of ``project-agents-writer``
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


SKILL_NAME = "project-agents-writer"
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
        assert "name: project-agents-writer" in testee_header

    def test_description(_, testee_header):
        print(testee_header)
        assert (
            'description: "Writes and maintains `AGENTS.md` files \\u2014'
            " concise, agent-readable repository context for AI coding"
            " tools covering setup, build, run, and test commands,"
            " conventions, tooling, and safety constraints, with required"
            ' frontmatter and a standard title."'
            in testee_header
        )

    def test_when_to_use(_, testee_header):
        print(testee_header)
        assert any(
            'when_to_use:' in line and 'documenting repo context for AI coding tools.' in line
            for line in testee_header
        )

    def test_paths(_, testee_header):
        assert (
            "paths:" in testee_header
            and "- '**/{AGENTS,Agents,agents}{,.md}'" in testee_header
        )

    def test_version(self, testee_header):
        assert any(VERSION_LINE_PATTERN.match(line) for line in testee_header)


class TestStructure:  # ========================================================

    def test_structure(_, testee_skill_file):
        assert assert_frontmatter_md_file_basic_structure(testee_skill_file)


class TestContent:  # =========================================================

    def test0(_, testee_content):
        assert TESTEE_FILE_CONTENT[0] in testee_content

class TestPrerequisite:  # ====================================================

    def test_heading(_, testee_content):
        assert "### {prerequisite}" in testee_content or "#### {prerequisite}" in testee_content

    def test0(_, testee_content):
        assert TESTEE_PREREQUISITE_CONTENT[0] in testee_content
