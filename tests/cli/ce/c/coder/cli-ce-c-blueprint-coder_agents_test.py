"""
cli-ce-c-blueprint-coder_agents_test.py

Unit Tests (using pytest) for:

creation of ``coder_agents_blueprint.md``
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
    with open(testee_rules_folder / "coder_agents_blueprint.md") as f:
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
        assert "name: Coder AGENTS Writer" in testee_header

    def test_description(_, testee_header):
        assert (
            "description: format for AGENTS.md documentation" in testee_header
        )

    def test_always_apply(_, testee_header):
        assert_header_line_always_apply(testee_header, False)


class TestContent:  # ==========================================================

    def test_heading(_, testee_content):
        assert "## Coder AGENTS Writer" in testee_content

    def test_intro_expert(_, testee_content):
        assert (
            "You are an expert in writing and maintaining `AGENTS.md` files"
            in testee_content
        )

    def test_purpose_section(_, testee_content):
        assert "#### Purpose" in testee_content

    def test_purpose_agent_readable(_, testee_content):
        assert (
            "`AGENTS.md` is a dedicated, agent-readable file that gives AI "
            "coding tools the context they need"
            in testee_content
        )

    def test_style_section(_, testee_content):
        assert "#### Style" in testee_content

    def test_style_guide_reference(_, testee_content):
        assert "Apply the provided **Style Guide**" in testee_content

    def test_style_briefness(_, testee_content):
        assert "Apply **Briefness Style** throughout" in testee_content

    def test_continue_rule_section(_, testee_content):
        assert "#### Continue Rule Compatible" in testee_content

    def test_document_title_section(_, testee_content):
        assert "#### Document Title" in testee_content

    def test_document_title_format(_, testee_content):
        assert "# <Project Name> AGENTS" in testee_content

    def test_quality_expectations_section(_, testee_content):
        assert "#### Quality Expectations" in testee_content
