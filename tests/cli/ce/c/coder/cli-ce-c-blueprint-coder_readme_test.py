"""
cli-ce-c-blueprint-coder_readme_test.py

Unit Tests (using pytest) for:

creation of ``coder_readme_blueprint.md``
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
    with open(testee_rules_folder / "coder_readme_blueprint.md") as f:
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
        assert "name: Coder README Writer" in testee_header

    def test_description(_, testee_header):
        assert "description: format for README documentation" in testee_header

    def test_always_apply(_, testee_header):
        assert_header_line_always_apply(testee_header, False)


class TestContent:  # ==========================================================

    def test_heading(_, testee_content):
        assert "## Coder README Writer" in testee_content

    def test_intro_expert(_, testee_content):
        assert (
            "You are an expert in writing and maintaining `README.md` files"
            in testee_content
        )

    def test_purpose_section(_, testee_content):
        assert "#### Purpose" in testee_content

    def test_purpose_landing_page(_, testee_content):
        assert (
            "`README.md` is a human-oriented landing page that helps developers"
            in testee_content
        )

    def test_style_section(_, testee_content):
        assert "#### Style" in testee_content

    def test_style_guide_reference(_, testee_content):
        assert "Apply the provided **Style Guide**" in testee_content

    def test_style_briefness(_, testee_content):
        assert "Apply **Briefness Style**" in testee_content

    def test_document_title_section(_, testee_content):
        assert "#### Document Title" in testee_content

    def test_document_title_format(_, testee_content):
        assert "# <Project Name> README" in testee_content

    def test_quality_expectations_section(_, testee_content):
        assert "#### Quality Expectations" in testee_content

    def test_quality_human_friendly(_, testee_content):
        assert (
            "human-friendly, visually clear, and easy to scan" in testee_content
        )
