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
            "Update README-style files, AGENTS-style files, and files under "
            "`docs/` to reflect the current project state"
            in testee_content
        )

    def test_instructions_section(_, testee_content):
        assert "##### Instructions" in testee_content

    def test_instructions_review_changes(_, testee_content):
        assert "review recent repository changes" in testee_content

    def test_instructions_edit_in_place(_, testee_content):
        assert (
            "edit existing documentation in place whenever possible"
            in testee_content
        )

    def test_readme_style_section(_, testee_content):
        assert "##### README-Style Files" in testee_content

    def test_readme_writer_reference(_, testee_content):
        assert (
            "follow **README Writer** for structure, content, and style"
            in testee_content
        )

    def test_agents_style_section(_, testee_content):
        assert "##### AGENTS-Style Files" in testee_content

    def test_agents_writer_reference(_, testee_content):
        assert (
            "follow **AGENTS Writer** for structure, content, and style"
            in testee_content
        )

    def test_docs_files_section(_, testee_content):
        assert "##### Docs Files" in testee_content

    def test_remove_stale_content(_, testee_content):
        assert (
            "remove stale, misleading, duplicated, obsolete, or unsupported "
            "content"
            in testee_content
        )
