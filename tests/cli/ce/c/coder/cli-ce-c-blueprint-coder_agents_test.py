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
        assert "## AGENTS Writer" in testee_content

    def test_intro_expert(_, testee_content):
        assert (
            "You are an expert in writing `AGENTS.md` files" in testee_content
        )

    def test_purpose_agent_readable(_, testee_content):
        assert (
            "`AGENTS.md` is a dedicated, agent-readable file" in testee_content
        )

    def test_style_commentary_case(_, testee_content):
        assert (
            "use **Commentary Case** for all list items and descriptions"
            in testee_content
        )

    def test_style_briefness(_, testee_content):
        assert "apply **Briefness Style** throughout" in testee_content

    def test_structure_project_overview(_, testee_content):
        assert "**Project Overview**" in testee_content

    def test_structure_build_and_test(_, testee_content):
        assert "**Build and Test Commands**" in testee_content

    def test_structure_security(_, testee_content):
        assert "**Security Considerations**" in testee_content

    def test_content_rules_exact_commands(_, testee_content):
        assert "prefer exact commands over vague descriptions" in testee_content

    def test_content_rules_monorepos(_, testee_content):
        assert (
            "for monorepos, recommend nested `AGENTS.md` files per subproject"
            in testee_content
        )

    def test_continue(_, testee_content):
        assert "#### Continue Rule Compatible" in testee_content
