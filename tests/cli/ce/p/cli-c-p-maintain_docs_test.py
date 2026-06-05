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

    def test_maintain_docs_heading(_, testee_content):
        assert "### Maintain Docs" in testee_content

    def test_review_recent_changes(_, testee_content):
        assert "review recent changes" in testee_content

    def test_update_or_create_readme(_, testee_content):
        assert "update or create `README.md`" in testee_content

    def test_docs_folder(_, testee_content):
        assert "files in `docs/`" in testee_content

    def test_update_or_create_agents_md(_, testee_content):
        assert "and `AGENTS.md`" in testee_content

    def test_reflect_changes(_, testee_content):
        assert "to reflect them" in testee_content

    def test_readme_focused_on_human_contributors(_, testee_content):
        assert (
            "Keep `README.md` focused on human contributors" in testee_content
        )

    def test_agents_md_writer_rule(_, testee_content):
        assert "Follow the *AGENTS.md Writer* rule" in testee_content

    def test_agents_md_structure_content_style(_, testee_content):
        assert "structure, content, and style" in testee_content

    def test_ensure_accuracy_remove_stale(_, testee_content):
        assert "Ensure accuracy, remove stale content" in testee_content
