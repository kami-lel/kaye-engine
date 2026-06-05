"""
cli-ce-c-abbr-currency_symbol_test.py

Unit Tests (using pytest) for:

creation of ``abbr-currency_symbol``
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
    with open(testee_rules_folder / "abbr-currency_symbol.md") as f:
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
        assert "name: Abbreviations Currency Symbols" in testee_header

    def test_always_apply(_, testee_header):
        assert_header_line_always_apply(testee_header, False)


class TestContent:  # ==========================================================

    def test1(_, testee_content):
        assert "- $:(default)US Dollar" in testee_content

    def test2(_, testee_content):
        assert "- HK$:港元 Hong Kong Dollar" in testee_content

    def test3(_, testee_content):
        assert "- JP¥:円 Japanese Yen" in testee_content

    def test4(_, testee_content):
        assert "- ¢:(default)US cent" in testee_content

    def test5(_, testee_content):
        assert "- ¤:any non-specific currency" in testee_content

    def test6(_, testee_content):
        assert "- ¥:(default)Chinese Yuan,RMB" in testee_content

    def test7(_, testee_content):
        assert "- €:Euro" in testee_content
