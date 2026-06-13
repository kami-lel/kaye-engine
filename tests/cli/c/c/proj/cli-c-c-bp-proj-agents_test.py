"""
cli-c-c-bp-proj-agents_test.py

Unit Tests (using pytest) for:

creation of ``Project AGENTS Writer.md``
"""

import pytest

from tests.cli import MD_FILENAME2SKILL_NAME
from tests.cli import (
    assert_frontmatter_md_file_basic_structure,
    split_frontmatter_md_file,
    assert_header_line_always_apply,
)

# constants  ###################################################################
MD_FILENAME = "project-agents-writer"
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
    return split_frontmatter_md_file(testee)[0]


@pytest.fixture(scope="session")
def testee_content(testee):
    return split_frontmatter_md_file(testee)[1]


# Pytest unit tests  ###########################################################


class TestBasic:  # ============================================================

    def test_existence(_, testee_path):
        assert testee_path.exists()

    def test_is_file(_, testee_path):
        assert testee_path.is_file()


class TestStructure:  # ========================================================

    def test_structure(_, testee):
        assert assert_frontmatter_md_file_basic_structure(testee)


class TestHeader:  # ===========================================================

    def test_name(_, testee_header):
        assert "name: Project AGENTS Writer" in testee_header

    def test_description(_, testee_header):
        assert (
            "description: format for AGENTS.md documentation" in testee_header
        )

    def test_always_apply(_, testee_header):
        assert_header_line_always_apply(testee_header, False)


class TestContent:  # ==========================================================

    def test_heading(_, testee_content):
        assert "## Project AGENTS Writer" in testee_content

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
