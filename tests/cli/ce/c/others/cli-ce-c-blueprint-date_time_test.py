"""
cli-ce-c-blueprint-date_time_test.py

Unit Tests (using pytest) for:

creation of ``Date and Time Format.md``
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
    with open(testee_rules_folder / "Date and Time Format.md") as f:
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
        assert "name: Date and Time Format" in testee_header

    def test_description(_, testee_header):
        assert (
            "description: when dates or times appear in output" in testee_header
        )

    def test_always_apply(_, testee_header):
        assert_header_line_always_apply(testee_header, False)


class TestContent:  # ==========================================================

    def test_date_time_format_heading(_, testee_content):
        assert "## Date and Time Format" in testee_content

    def test_full_date_example(_, testee_content):
        assert "- Full Date Example:" in testee_content

    def test_full_date_format(_, testee_content):
        assert "`Mon 02015-01-15`" in testee_content

    def test_month_day_example(_, testee_content):
        assert "- Month-Day Example:" in testee_content

    def test_month_day_format(_, testee_content):
        assert "`Tue 01-16`" in testee_content

    def test_time_format(_, testee_content):
        assert "- Time Format:" in testee_content

    def test_24_hour_clock(_, testee_content):
        assert "24-hour clock" in testee_content
