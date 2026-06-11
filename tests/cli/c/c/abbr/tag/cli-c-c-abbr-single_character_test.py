"""
cli-c-c-abbr-single_character_test.py

Unit Tests (using pytest) for:

creation of ``abbr-single_character``
"""

import pytest

from tests.cli import MD_FILENAME2SKILL_NAME
from tests.cli.c.c import (
    assert_rule_file_basic_format,
    split_rule_file_basic_format,
    assert_header_line_always_apply,
)

# constants  ###################################################################
MD_FILENAME = "abbr-single-character"
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
        assert "name: Abbr Single Character" in testee_header

    def test_always_apply(_, testee_header):
        assert_header_line_always_apply(testee_header, False)


class TestContent:  # ==========================================================

    def test_dollar(_, testee_content):
        assert "- $:(default)US Dollar" in testee_content

    def test_ampersand(_, testee_content):
        assert "- &:and" in testee_content

    def test_greater_than(_, testee_content):
        assert "- >:greater than" in testee_content

    def test_b_bit(_, testee_content):
        assert "- b:bit" in testee_content

    def test_C_can(_, testee_content):
        assert "- C:can,could" in testee_content

    def test_degree(_, testee_content):
        assert "- °:degree" in testee_content

    def test_section(_, testee_content):
        assert "- §:chapter" in testee_content

    def test_multiply(_, testee_content):
        assert "- ×:multiply,multiplication,multiplier" in testee_content

    def test_rightwards_double_arrow(_, testee_content):
        assert "- ⇒:therefore,causing,resulting" in testee_content

    def test_ditto(_, testee_content):
        assert "- 〃:ditto,repetitive as above" in testee_content
