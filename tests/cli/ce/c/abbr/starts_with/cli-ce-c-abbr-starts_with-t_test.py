"""
cli-ce-c-abbr-starts_with-t_test.py

Unit Tests (using pytest) for:

creation of ``abbr-starts_with-t``
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
    with open(testee_rules_folder / "Abbr Starts with T.md") as f:
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
