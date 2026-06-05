"""
cli-ce-c-abbr-starts_with-i_test.py

Unit Tests (using pytest) for:

creation of ``abbr-starts_with-i``
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
    with open(testee_rules_folder / "abbr-starts_with-i.md") as f:
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
        assert "name: Abbreviations Starts with I" in testee_header

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
