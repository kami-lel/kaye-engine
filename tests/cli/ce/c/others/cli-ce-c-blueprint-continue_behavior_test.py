"""
cli-ce-c-blueprint-continue_behavior_test.py

Unit Tests (using pytest) for:

creation of ``Continue Behavior.md``
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
    with open(testee_rules_folder / "Continue Behavior.md") as f:
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
        assert "name: Continue Behavior" in testee_header

    def test_always_apply(_, testee_header):
        assert_header_line_always_apply(testee_header, True)


class TestContent:  # ==========================================================

    def test_heading(_, testee_content):
        assert "## Continue Behavior" in testee_content

    def test_file_consistency_rule(_, testee_content):
        assert (
            "Files are assumed to be consistent between rounds."
            in testee_content
        )

    def test_intentional_edits_rule(_, testee_content):
        assert "treat them as intentional user edits" in testee_content

    def test_run_terminal_command_heading(_, testee_content):
        assert "#### `run_terminal_command`" in testee_content

    def test_last_resort_rule(_, testee_content):
        assert (
            "Only use `run_terminal_command` as a last resort" in testee_content
        )

    def test_delete_use_case(_, testee_content):
        assert "Use when need to remove/delete file/folder." in testee_content
