"""
cli-c-p-maintain_docs_test.py

Unit Tests (using pytest) for:

creation of ``maintain_docs.md``
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
    with open(testee_prompts_folder / "maintain_docs.md") as f:
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
        assert "name: Maintain Docs" in testee_header

    def test_always_apply(_, testee_header):
        assert_header_line_always_apply(testee_header, False)

    def test_invokable(_, testee_header, header_invokable_line):
        assert header_invokable_line in testee_header


class TestContent:  # ==========================================================

    def test_heading(_, testee_content):
        assert "### Maintain Docs" in testee_content

    def test_intro_readme_agents_docs(_, testee_content):
        assert (
            "Update README-style files, AGENTS-style files, "
            "and files under `docs/`"
            in testee_content
        )

    def test_instructions_section(_, testee_content):
        assert "##### Instructions" in testee_content

    def test_instructions_review_changes(_, testee_content):
        assert "review recent repository changes" in testee_content

    def test_instructions_create_only_when_missing(_, testee_content):
        assert (
            "create new documentation only when an important expected file "
            "is missing or repository changes require it"
            in testee_content
        )

    def test_instructions_readme_style_definition(_, testee_content):
        assert (
            "treat README-style files as files named `README`, `Readme`, or "
            "`readme`, with no extension, `.md`, or `.txt`"
            in testee_content
        )

    def test_instructions_agents_style_definition(_, testee_content):
        assert (
            "treat AGENTS-style files as files named `AGENTS`, `Agents`, or "
            "`agents`, with no extension or `.md`"
            in testee_content
        )

    def test_instructions_verify_content(_, testee_content):
        assert (
            "verify links, file paths, commands, configuration names, "
            "examples, and references where possible"
            in testee_content
        )

    def test_docs_files_section(_, testee_content):
        assert "##### Docs Files" in testee_content

    def test_docs_files_update_affected(_, testee_content):
        assert (
            "update affected APIs, commands, architecture notes, configuration "
            "details, examples, workflows, and troubleshooting guidance"
            in testee_content
        )

    def test_docs_files_cross_link(_, testee_content):
        assert (
            "cross-link related docs when it improves navigation"
            in testee_content
        )

    def test_output_section(_, testee_content):
        assert "##### Output" in testee_content

    # edit README  -------------------------------------------------------------

    def test_edit_readme_section(_, testee_content):
        assert "#### edit README" in testee_content

    def test_edit_readme_follow_writer(_, testee_content):
        assert (
            "follow **README Writer** for structure, content, and style"
            in testee_content
        )

    def test_edit_readme_update_applicable(_, testee_content):
        assert (
            "update applicable overview, features, setup, usage, "
            "configuration, commands, contribution notes, security notes, and "
            "license details"
            in testee_content
        )

    def test_edit_readme_prioritize_root(_, testee_content):
        assert (
            "prioritize the root README when multiple README-style files exist"
            in testee_content
        )

    # edit AGENTS  -------------------------------------------------------------

    def test_edit_agents_section(_, testee_content):
        assert "#### edit AGENTS" in testee_content

    def test_edit_agents_follow_writer(_, testee_content):
        assert (
            "follow **AGENTS Writer** for structure, content, and style"
            in testee_content
        )

    def test_edit_agents_preserve_frontmatter(_, testee_content):
        assert (
            "preserve or add required frontmatter when applicable"
            in testee_content
        )

    def test_edit_agents_avoid_moving_content(_, testee_content):
        assert (
            "avoid moving human-facing content from README files into AGENTS "
            "files unless it is useful for coding agents"
            in testee_content
        )
