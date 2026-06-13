"""
cli-c-c-abbr-starts_with-t_test.py

Unit Tests (using pytest) for:

creation of ``abbr-starts_with-t``
"""

import pytest

from tests.cli import MD_FILENAME2SKILL_NAME
from tests.cli import (
    assert_frontmatter_md_file_basic_structure,
    split_frontmatter_md_file,
    assert_header_line_always_apply,
)

# constants  ###################################################################
MD_FILENAME = "abbr-starts-with-t"
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
        assert "name: Abbr Starts with T" in testee_header

    def test_always_apply(_, testee_header):
        assert_header_line_always_apply(testee_header, False)


class TestContent:  # ==========================================================

    def test_T_than(_, testee_content):
        assert "- T:than" in testee_content

    def test_T_true(_, testee_content):
        assert "- T:true" in testee_content

    def test_tech(_, testee_content):
        assert "- tech:technology" in testee_content

    def test_tf(_, testee_content):
        assert "- tf:therefore,causing,resulting" in testee_content

    def test_tho(_, testee_content):
        assert "- tho:though" in testee_content

    def test_thru(_, testee_content):
        assert "- thru:through" in testee_content

    def test_tmp(_, testee_content):
        assert "- tmp:temporary" in testee_content

    def test_tr(_, testee_content):
        assert "- tr:translate" in testee_content

    def test_tt(_, testee_content):
        assert "- tt:that,those" in testee_content

    def test_txt(_, testee_content):
        assert "- txt:text" in testee_content
