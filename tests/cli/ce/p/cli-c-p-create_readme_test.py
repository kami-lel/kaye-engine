"""
cli-c-p-create_readme_test.py

Unit Tests (using pytest) for:

creation of ``create_readme.md``
"""

import pytest

from tests.cli.ce.c import (
    assert_rule_file_basic_format,
    split_rule_file_basic_format,
    assert_header_line_always_apply,
)

# Pytest fixtures  #############################################################


@pytest.fixture(scope="session")
def testee(testee_prompts_folder):
    with open(testee_prompts_folder / "create_readme.md") as f:
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
        assert "name: Create README" in testee_header

    def test_always_apply(_, testee_header):
        assert_header_line_always_apply(testee_header, False)

    def test_invokable(_, testee_header, header_invokable_line):
        assert header_invokable_line in testee_header


class TestContent:  # ==========================================================

    def test_heading(_, testee_content):
        assert "### Create README" in testee_content

    def test_intro_readme_writer(_, testee_content):
        assert (
            "Use **README Writer** as the guideline for what makes a good "
            "`README.md`"
            in testee_content
        )

    def test_instructions_section(_, testee_content):
        assert "##### Instructions" in testee_content

    def test_instructions_create_complete(_, testee_content):
        assert (
            "create a complete new `README.md` tailored to the repository"
            in testee_content
        )

    def test_instructions_human_oriented(_, testee_content):
        assert (
            "make the README human-oriented, visually clear, and easy to scan"
            in testee_content
        )

    def test_structure_guidelines_section(_, testee_content):
        assert "##### Structure Guidelines" in testee_content

    def test_project_overview_guideline(_, testee_content):
        assert "**Project Overview**" in testee_content

    def test_features_guideline(_, testee_content):
        assert "**Features**" in testee_content

    def test_getting_started_guideline(_, testee_content):
        assert "**Getting Started**" in testee_content

    def test_installation_guideline(_, testee_content):
        assert "**Installation**" in testee_content

    def test_usage_guideline(_, testee_content):
        assert "**Usage**" in testee_content

    def test_contributing_guideline(_, testee_content):
        assert "**Contributing**" in testee_content

    def test_security_guideline(_, testee_content):
        assert "**Security**" in testee_content

    def test_license_guideline(_, testee_content):
        assert "**License**" in testee_content

    def test_build_test_commands_guideline(_, testee_content):
        assert "**Build and Test Commands**" in testee_content

    def test_output_section(_, testee_content):
        assert "###### Output" in testee_content

    def test_output_file_location(_, testee_content):
        assert "Create the `README.md` file at the project root" \
            in testee_content
