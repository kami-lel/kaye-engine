"""
cli-ce-c-abbr-starts_with-f_test.py

Unit Tests (using pytest) for:

creation of ``abbr-starts_with-f``
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
    with open(testee_rules_folder / "Abbr Starts with F.md") as f:
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
        assert "name: Abbr Starts with F" in testee_header

    def test_always_apply(_, testee_header):
        assert_header_line_always_apply(testee_header, False)


class TestContent:  # ==========================================================

    def test_F_fall(_, testee_content):
        assert "- F:fall" in testee_content

    def test_F_false(_, testee_content):
        assert "- F:false" in testee_content

    def test_fd(_, testee_content):
        assert "- fd:find,found" in testee_content

    def test_fm(_, testee_content):
        assert "- fm:formal" in testee_content

    def test_fmt(_, testee_content):
        assert "- fmt:format,formatting" in testee_content

    def test_fr(_, testee_content):
        assert "- fr:from" in testee_content

    def test_frq(_, testee_content):
        assert "- frq:frequent,frequently,frequency" in testee_content

    def test_fx(_, testee_content):
        assert "- fx:function" in testee_content
