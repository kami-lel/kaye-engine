"""
cli-c-c-bp-continue-behavior_test.py

Unit Tests (using pytest) for:

creation of ``Continue Behavior.md``
"""

import pytest

from tests.cli import MD_FILENAME2SKILL_NAME
from tests.cli.c.c import (
    assert_rule_file_basic_format,
    split_rule_file_basic_format,
    assert_header_line_always_apply,
)

# constants  ###################################################################
MD_FILENAME = "continue-behavior"
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
        assert "# Continue Behavior" in testee_content

    def test_run_terminal_command_heading(_, testee_content):
        assert "### `run_terminal_command`" in testee_content

    def test_last_resort_rule(_, testee_content):
        assert (
            "Only use `run_terminal_command` as a last resort" in testee_content
        )

    def test_delete_use_case(_, testee_content):
        assert "Use when need to remove/delete file/folder." in testee_content
