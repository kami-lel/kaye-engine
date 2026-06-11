"""
cli-c-c-abbr-starts_with-digits_test.py

Unit Tests (using pytest) for:

creation of ``abbr-starts_with-digits``
"""

import pytest

from tests.cli.c.c import (
    assert_rule_file_basic_format,
    split_rule_file_basic_format,
    assert_header_line_always_apply,
)

# Pytest fixtures  #############################################################


@pytest.fixture(scope="session")
def testee(testee_rules_folder):

    with open(testee_rules_folder / "Abbr Starts with Digits 0~9.md") as f:
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
        assert "name: Abbr Starts with Digits 0~9" in testee_header

    def test_always_apply(_, testee_header):
        assert_header_line_always_apply(testee_header, False)


class TestContent:  # ==========================================================

    def test_2_to(_, testee_content):
        assert "- 2:to" in testee_content

    def test_2_too(_, testee_content):
        assert "- 2:too" in testee_content

    def test_4(_, testee_content):
        assert "- 4:for" in testee_content
