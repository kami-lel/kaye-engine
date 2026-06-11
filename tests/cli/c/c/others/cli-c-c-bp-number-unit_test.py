"""
cli-c-c-bp-number-unit_test.py

Unit Tests (using pytest) for:

creation of ``Numerical Values with Units.md``
"""

import pytest

from tests.cli import MD_FILENAME2SKILL_NAME
from tests.cli.c.c import (
    assert_rule_file_basic_format,
    split_rule_file_basic_format,
    assert_header_line_always_apply,
)

# constants  ###################################################################
MD_FILENAME = "numerical-values-with-units"
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


class TestBasic:  # ============================================================

    def test_existence(_, testee_path):
        assert testee_path.exists()

    def test_is_file(_, testee_path):
        assert testee_path.is_file()

    def test_structure(_, testee):
        assert assert_rule_file_basic_format(testee)


class TestHeader:  # ===========================================================

    def test_name(_, testee_header):
        assert "name: Numerical Values with Units" in testee_header

    def test_description(_, testee_header):
        assert (
            "description: when physical quantities appear in output"
            in testee_header
        )

    def test_always_apply(_, testee_header):
        assert_header_line_always_apply(testee_header, False)


class TestContent:  # ==========================================================

    def test_numerical_values_heading(_, testee_content):
        assert "## Numerical Values with Units" in testee_content

    def test_dual_unit_systems(_, testee_content):
        assert "- Dual Unit Systems:" in testee_content

    def test_distance_example(_, testee_content):
        assert "- Distance: `8 848m (29 029ft)`" in testee_content

    def test_unit_abbreviations(_, testee_content):
        assert "- Unit Abbreviations:" in testee_content

    def test_thousands_separator(_, testee_content):
        assert "- Thousands Separator:" in testee_content

    def test_space_separator(_, testee_content):
        assert (
            "Use a space character as the thousands separator" in testee_content
        )
