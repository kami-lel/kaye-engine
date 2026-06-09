"""
cli-ce-c-abbr-symbol_test.py

Unit Tests (using pytest) for:

creation of ``abbr-symbol``
"""

import pytest

from tests.cli.ce.c import (
    assert_rule_file_basic_format,
    split_rule_file_basic_format,
    assert_header_line_always_apply,
)

# Pytest fixtures  #############################################################


@pytest.fixture(scope="session")
def testee(testee_rules_folder):
    with open(testee_rules_folder / "Abbr Symbols.md") as f:
        return f.read()


@pytest.fixture(scope="session")
def testee_header(testee):
    return split_rule_file_basic_format(testee)[0]


@pytest.fixture(scope="session")
def testee_content(testee):
    return split_rule_file_basic_format(testee)[1]


# Pytest unit tests  ###########################################################


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
