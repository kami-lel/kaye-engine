"""
cli-c-c-bp-role-assistant-barista_test.py

Unit Tests (using pytest) for:

creation of ``Assistant Barista.md``
"""

import pytest

from tests.cli import MD_FILENAME2SKILL_NAME, TESTEE_FILE_CONTENT_ALL
from tests.cli import (
    assert_frontmatter_md_file_basic_structure,
    split_frontmatter_md_file,
    assert_header_line_always_apply,
)

# constants  ###################################################################
MD_FILENAME = "assistant-barista"
_SKILL_NAME = MD_FILENAME2SKILL_NAME[MD_FILENAME]
TESTEE_FILE_CONTENT = TESTEE_FILE_CONTENT_ALL[MD_FILENAME]

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
        assert "name: Assistant Barista" in testee_header

    def test_description(_, testee_header):
        assert any("coffee brewing note" in line for line in testee_header)

    def test_always_apply(_, testee_header):
        assert_header_line_always_apply(testee_header, False)


class TestContent:  # ==========================================================

    def test0(_, testee_content):
        assert TESTEE_FILE_CONTENT[0] in testee_content

    def test1(_, testee_content):
        assert TESTEE_FILE_CONTENT[1] in testee_content

    def test2(_, testee_content):
        assert TESTEE_FILE_CONTENT[2] in testee_content
