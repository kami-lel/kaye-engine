"""
cli-c-c-abbr-symbol_test.py

Unit Tests (using pytest) for:

creation of ``abbr-symbol``
"""

import pytest

from tests.cli import MD_FILENAME2SKILL_NAME
from tests.cli.c.c import (
    assert_rule_file_basic_format,
    split_rule_file_basic_format,
    assert_header_line_always_apply,
)

# constants  ###################################################################
MD_FILENAME = "abbr-symbols"
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
    return split_rule_file_basic_format(testee)[0]


@pytest.fixture(scope="session")
def testee_content(testee):
    return split_rule_file_basic_format(testee)[1]


# Pytest unit tests  ###########################################################


class TestBasic:  # ============================================================

    def test_existence(_, testee_path):
        assert testee_path.exists()

    def test_is_file(_, testee_path):
        assert testee_path.is_file()


class TestStructure:  # ========================================================

    def test_structure(_, testee):
        assert assert_rule_file_basic_format(testee)


class TestHeader:  # ===========================================================

    def test_name(_, testee_header):
        assert "name: Abbr Symbols" in testee_header

    def test_always_apply(_, testee_header):
        assert_header_line_always_apply(testee_header, False)


class TestContent:  # ==========================================================

    def test_exclamation(_, testee_content):
        assert "- !:no,not,incorrect" in testee_content

    def test_not_equal(_, testee_content):
        assert "- !=:not equal" in testee_content

    def test_ampersand(_, testee_content):
        assert "- &:and" in testee_content

    def test_arrow_right(_, testee_content):
        assert "- ->:become/change/transform into" in testee_content

    def test_arrow_left(_, testee_content):
        assert "- <-:become/change/transform from" in testee_content

    def test_therefore(_, testee_content):
        assert "- =>:therefore,causing,resulting" in testee_content

    def test_sqrt(_, testee_content):
        assert "- √:square root" in testee_content

    def test_infinite(_, testee_content):
        assert "- ∞:infinite" in testee_content

    def test_warning(_, testee_content):
        assert "- ⚠️:warning" in testee_content

    def test_checkmark(_, testee_content):
        assert "- ✓:correct,correction" in testee_content
