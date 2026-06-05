"""
cli-ce-c-blueprint-number_unit_test.py

Unit Tests (using pytest) for:

creation of ``number_unit_blueprint.md``
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
    with open(testee_rules_folder / "number_unit_blueprint.md") as f:
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
        assert "name: Numerical Values with Units" in testee_header

    def test_description(_, testee_header):
        assert (
            "description: add-on when physical quantities appear in output"
            in testee_header
        )

    def test_always_apply(_, testee_header):
        assert_header_line_always_apply(testee_header, False)


class TestContent:  # ==========================================================

    def test_elements_heading(_, testee_content):
        assert "# Elements" in testee_content

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
        assert "Use a space character as the thousands separator" \
            in testee_content
