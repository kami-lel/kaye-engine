"""
cli-c-c-abbr-unit_of_measure_test.py

Unit Tests (using pytest) for:

creation of ``abbr-unit_of_measure``
"""

import pytest

from tests.cli import MD_FILENAME2SKILL_NAME
from tests.cli.c.c import (
    assert_rule_file_basic_format,
    split_rule_file_basic_format,
    assert_header_line_always_apply,
)

# constants  ###################################################################
MD_FILENAME = "abbr-units-of-measure"
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


class TestStructure:  # ========================================================

    def test_structure(_, testee):
        assert assert_rule_file_basic_format(testee)


class TestHeader:  # ===========================================================

    def test_name(_, testee_header):
        assert "name: Abbr Units of Measure" in testee_header

    def test_always_apply(_, testee_header):
        assert_header_line_always_apply(testee_header, False)


class TestContent:  # ==========================================================

    def test_b_bit(_, testee_content):
        assert "- b:bit" in testee_content

    def test_B_byte(_, testee_content):
        assert "- B:byte" in testee_content

    def test_ft(_, testee_content):
        assert "- ft:foot" in testee_content

    def test_hr(_, testee_content):
        assert "- hr:hour" in testee_content

    def test_lb(_, testee_content):
        assert "- lb:pound" in testee_content

    def test_mi(_, testee_content):
        assert "- mi:mile" in testee_content

    def test_min(_, testee_content):
        assert "- min:minute" in testee_content

    def test_s(_, testee_content):
        assert "- s:second" in testee_content

    def test_yd(_, testee_content):
        assert "- yd:yard" in testee_content

    def test_nmi(_, testee_content):
        assert "- nmi:nautical mile" in testee_content
