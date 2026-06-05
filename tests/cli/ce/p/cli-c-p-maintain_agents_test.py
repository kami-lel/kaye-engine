"""
cli-c-p-maintain_agents_test.py

Unit Tests (using pytest) for:

creation of ``maintain_agents.md``
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
    with open(testee_prompts_folder / "maintain_agents.md") as f:
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
        assert "name: Maintain Agents" in testee_header

    def test_always_apply(_, testee_header):
        assert_header_line_always_apply(testee_header, False)

    def test_invokable(_, testee_header, header_invokable_line):
        assert header_invokable_line in testee_header


class TestContent:  # ==========================================================

    def test_maintain_agents_heading(_, testee_content):
        assert "### Maintain Agents" in testee_content

    def test_review_recent_changes(_, testee_content):
        assert "review recent changes" in testee_content

    def test_update_or_create_agents_md(_, testee_content):
        assert "update or create `AGENTS.md`" in testee_content

    def test_reflect_changes(_, testee_content):
        assert "to reflect them" in testee_content

    def test_agents_md_writer_rule(_, testee_content):
        assert "Follow the *AGENTS.md Writer* rule" in testee_content

    def test_structure_content_style(_, testee_content):
        assert "structure, content, and style" in testee_content
