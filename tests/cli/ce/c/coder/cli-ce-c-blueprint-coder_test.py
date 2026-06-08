"""
cli-ce-c-blueprint-coder_test.py

Unit Tests (using pytest) for:

creation of ``coder_blueprint.md``
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
    with open(testee_rules_folder / "coder_blueprint.md") as f:
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
        assert "name: Kaye Peer Coder" in testee_header

    def test_description(_, testee_header):
        assert (
            "description: instruction for coding and programming"
            in testee_header
        )

    def test_always_apply(_, testee_header):
        assert_header_line_always_apply(testee_header, True)


class TestContent:  # ==========================================================

    def test_heading(_, testee_content):
        assert "# Kaye Peer Coder" in testee_content

    def test_duty_expansion(_, testee_content):
        assert "- provide code **expansion**" in testee_content

    def test_duty_adjustment(_, testee_content):
        assert "- perform code **adjustment**" in testee_content

    def test_duty_support(_, testee_content):
        assert "- offer concise coding **support**" in testee_content

    def test_duty_debug(_, testee_content):
        assert "- help users **debug**" in testee_content

    def test_code_format_heading(_, testee_content):
        assert "### code format" in testee_content

    def test_80_char_limit(_, testee_content):
        assert "- each line must not exceed **80 characters**" in testee_content

    def test_variable_naming_heading(_, testee_content):
        assert "### variable naming" in testee_content

    def test_code_comment_heading(_, testee_content):
        assert "### code comment" in testee_content

    def test_csh_heading(_, testee_content):
        assert "### comment section headings" in testee_content
