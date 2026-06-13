"""
cli-c-c-abbr-starts_with-i_test.py

Unit Tests (using pytest) for:

creation of ``abbr-starts_with-i``
"""

import pytest

from tests.cli import MD_FILENAME2SKILL_NAME
from tests.cli import (
    assert_frontmatter_md_file_basic_structure,
    split_frontmatter_md_file,
    assert_header_line_always_apply,
)

# constants  ###################################################################
MD_FILENAME = "abbr-starts-with-i"
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
        assert "name: Abbr Starts with I" in testee_header

    def test_always_apply(_, testee_header):
        assert_header_line_always_apply(testee_header, False)


class TestContent:  # ==========================================================

    def test_i_e(_, testee_content):
        assert "- i.e.:that is,in other words" in testee_content

    def test_id(_, testee_content):
        assert "- id:identity,identification" in testee_content

    def test_ie(_, testee_content):
        assert "- ie:that is,in other words" in testee_content

    def test_iff(_, testee_content):
        assert "- iff:if and only if" in testee_content

    def test_info(_, testee_content):
        assert "- info:information,informational" in testee_content

    def test_int_integer(_, testee_content):
        assert "- int:integer" in testee_content

    def test_ipt(_, testee_content):
        assert "- ipt:input" in testee_content

    def test_iss(_, testee_content):
        assert "- iss:issue" in testee_content

    def test_icl(_, testee_content):
        assert "- icl:include,inclusion" in testee_content

    def test_inf(_, testee_content):
        assert "- inf:infinite" in testee_content
