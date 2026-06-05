"""
cli-ce-c-blueprint-coder_bash_test.py

Unit Tests (using pytest) for:

creation of ``coder_bash_blueprint.md``
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
    with open(testee_rules_folder / "coder_bash_blueprint.md") as f:
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
        assert "name: Coder Bash" in testee_header

    def test_description(_, testee_header):
        assert (
            "description: Debian GNU/Linux shell commands; ready-to-run output"
            in testee_header
        )

    def test_always_apply(_, testee_header):
        assert_header_line_always_apply(testee_header, False)


class TestContent:  # ==========================================================

    def test_heading(_, testee_content):
        assert "## Bash" in testee_content

    def test_debian_only(_, testee_content):
        assert "Debian GNU/Linux only" in testee_content

    def test_gnu_tools(_, testee_content):
        assert "Use standard GNU and Debian tools only." in testee_content

    def test_no_explanation(_, testee_content):
        assert (
            "Return only the command or commands, with no explanation."
            in testee_content
        )

    def test_sudo(_, testee_content):
        assert "Use sudo when needed." in testee_content

    def test_clarifying_question(_, testee_content):
        assert "ask one short clarifying question" in testee_content
