"""
cli-c-c-abbr-language_code_test.py

Unit Tests (using pytest) for:

creation of ``abbr-language_code``
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
    with open(testee_rules_folder / "Abbr Natural Language Codes.md") as f:
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
        assert "name: Abbr Natural Language Codes" in testee_header

    def test_always_apply(_, testee_header):
        assert_header_line_always_apply(testee_header, False)


class TestContent:  # ==========================================================

    def test_de(_, testee_content):
        assert "- de:Deutsch" in testee_content

    def test_en(_, testee_content):
        assert "- en:English" in testee_content

    def test_jp(_, testee_content):
        assert "- jp:日本語" in testee_content

    def test_zh(_, testee_content):
        assert "- zh:中文" in testee_content

    def test_zhs(_, testee_content):
        assert "- zhs:大陆简体中文" in testee_content

    def test_zht(_, testee_content):
        assert "- zht:香港繁體中文" in testee_content
