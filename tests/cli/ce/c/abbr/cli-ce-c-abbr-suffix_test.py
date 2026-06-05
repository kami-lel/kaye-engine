"""
cli-ce-c-abbr-suffix_test.py

Unit Tests (using pytest) for:

creation of ``abbr-suffix``
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
    with open(testee_rules_folder / "abbr-suffix.md") as f:
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
        assert "name: Abbreviations Suffixes" in testee_header

    def test_always_apply(_, testee_header):
        assert_header_line_always_apply(testee_header, False)


class TestContent:  # ==========================================================

    def test_d(_, testee_content):
        assert "- .d:-ed" in testee_content

    def test_e(_, testee_content):
        assert "- .e:-able,-ble,-le" in testee_content

    def test_g(_, testee_content):
        assert "- .g:-ing" in testee_content

    def test_l(_, testee_content):
        assert "- .l:-al" in testee_content

    def test_m(_, testee_content):
        assert "- .m:-ism" in testee_content

    def test_mt(_, testee_content):
        assert "- .mt:-ment" in testee_content

    def test_r(_, testee_content):
        assert "- .r:-er,-or" in testee_content

    def test_sn(_, testee_content):
        assert "- .sn:-sion" in testee_content

    def test_tn(_, testee_content):
        assert "- .tn:-tion" in testee_content

    def test_y_ly(_, testee_content):
        assert "- .y:-ly" in testee_content
