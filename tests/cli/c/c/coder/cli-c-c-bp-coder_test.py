"""
cli-c-c-bp-coder_test.py

Unit Tests (using pytest) for:

creation of ``Kaye Peer Coder.md``
"""

import pytest

from tests.cli import MD_FILENAME2SKILL_NAME
from tests.cli import (
    assert_frontmatter_md_file_basic_structure,
    split_frontmatter_md_file,
    assert_header_line_always_apply,
)

# constants  ###################################################################
MD_FILENAME = "kaye-peer-coder"
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
        assert "name: Kaye Peer Coder" in testee_header

    def test_description(_, testee_header):
        assert (
            "description: instruction for coding and programming"
            in testee_header
        )

    def test_always_apply(_, testee_header):
        assert_header_line_always_apply(testee_header, True)


class TestContent:  # ==========================================================

    def test_heading(_, testee_content):
        assert "# Kaye Peer Coder" in testee_content

    def test_duty_expansion(_, testee_content):
        assert "- provide code **expansion**" in testee_content

    def test_duty_adjustment(_, testee_content):
        assert "- perform code **adjustment**" in testee_content

    def test_duty_support(_, testee_content):
        assert "- offer concise coding **support**" in testee_content

    def test_duty_debug(_, testee_content):
        assert "- help users **debug**" in testee_content

    def test_code_format_heading(_, testee_content):
        assert "### code format" in testee_content

    def test_80_char_limit(_, testee_content):
        assert "- each line must not exceed **80 characters**" in testee_content

    def test_variable_naming_heading(_, testee_content):
        assert "### variable naming" in testee_content

    def test_code_comment_heading(_, testee_content):
        assert "### code comment" in testee_content

    def test_csh_heading(_, testee_content):
        assert "### comment section headings" in testee_content
