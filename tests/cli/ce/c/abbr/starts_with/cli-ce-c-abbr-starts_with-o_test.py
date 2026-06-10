"""
cli-ce-c-abbr-starts_with-o_test.py

Unit Tests (using pytest) for:

creation of ``abbr-starts_with-o``
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
    with open(testee_rules_folder / "Abbr Starts with O.md") as f:
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
        assert "name: Abbr Starts with O" in testee_header

    def test_always_apply(_, testee_header):
        assert_header_line_always_apply(testee_header, False)


class TestContent:  # ==========================================================

    def test_O(_, testee_content):
        assert "- O:only" in testee_content

    def test_obj(_, testee_content):
        assert "- obj:object" in testee_content

    def test_op(_, testee_content):
        assert "- op:operate,operation,operator" in testee_content

    def test_opmz(_, testee_content):
        assert "- opmz:optimize,optimization" in testee_content

    def test_opn_opinion(_, testee_content):
        assert "- opn:opinion" in testee_content

    def test_opp(_, testee_content):
        assert "- opp:oppose,opposition" in testee_content

    def test_opt(_, testee_content):
        assert "- opt:output" in testee_content

    def test_org(_, testee_content):
        assert "- org:organization" in testee_content

    def test_ori(_, testee_content):
        assert "- ori:origin,original" in testee_content

    def test_ot(_, testee_content):
        assert "- ot:other" in testee_content
