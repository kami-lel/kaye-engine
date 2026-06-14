"""
cli-c-c-bp-proj-agents_test.py

Unit Tests (using pytest) for:

creation of ``Project AGENTS Writer.md``
"""

import pytest

from tests.cli import MD_FILENAME2SKILL_NAME
from tests.cli import (
    TESTEE_FILE_CONTENT_ALL,
    assert_frontmatter_md_file_basic_structure,
    split_frontmatter_md_file,
    assert_header_line_always_apply,
)

# constants  ###################################################################
MD_FILENAME = "project-agents-writer"
TESTEE_FILE_CONTENT = TESTEE_FILE_CONTENT_ALL[MD_FILENAME]
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


class TestStructure:  # ========================================================

    def test_structure(_, testee):
        assert assert_frontmatter_md_file_basic_structure(testee)


class TestHeader:  # ===========================================================

    def test_name(_, testee_header):
        assert "name: Project AGENTS Writer" in testee_header

    def test_description(_, testee_header):
        print(testee_header)
        assert (
            'description: "Writes and maintains `AGENTS.md` files \\u2014'
            " concise, agent-readable repository context for AI coding"
            " tools covering setup, build, run, and test commands,"
            " conventions, tooling, and safety constraints, with required"
            " frontmatter and a standard title.\\u21B5Use when creating,"
            " updating, or reviewing an `AGENTS.md` or equivalent"
            ' agent-instruction file. Triggers: \\"write an AGENTS.md,\\"'
            ' \\"add agent instructions,\\" documenting repo context for'
            ' AI coding tools."'
            in testee_header
        )

    def test_always_apply(_, testee_header):
        assert_header_line_always_apply(testee_header, False)


class TestContent:  # =========================================================

    def test0(_, testee_content):
        assert TESTEE_FILE_CONTENT[0] in testee_content

    def test1(_, testee_content):
        assert TESTEE_FILE_CONTENT[1] in testee_content

    def test2(_, testee_content):
        assert TESTEE_FILE_CONTENT[2] in testee_content

    def test3(_, testee_content):
        assert TESTEE_FILE_CONTENT[3] in testee_content

    def test4(_, testee_content):
        assert TESTEE_FILE_CONTENT[4] in testee_content

    def test5(_, testee_content):
        assert TESTEE_FILE_CONTENT[5] in testee_content

    def test6(_, testee_content):
        assert TESTEE_FILE_CONTENT[6] in testee_content

    def test7(_, testee_content):
        assert TESTEE_FILE_CONTENT[7] in testee_content

    def test8(_, testee_content):
        assert TESTEE_FILE_CONTENT[8] in testee_content

    def test9(_, testee_content):
        assert TESTEE_FILE_CONTENT[9] in testee_content