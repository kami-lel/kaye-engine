"""
cli-ce-c-blueprint-coder_changelog_test.py

Unit Tests (using pytest) for:

creation of ``Coder CHANGELOG Writer.md``
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
    with open(testee_rules_folder / "Coder CHANGELOG Writer.md") as f:
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
        assert "name: Coder CHANGELOG Writer" in testee_header

    def test_description(_, testee_header):
        assert "description: format for CHANGELOG.md" in testee_header

    def test_globs(_, testee_header):
        assert (
            'globs: ["**/{CHANGELOG,Changelog,changelog}{,.md,.txt}"]'
            in testee_header
        )

    def test_always_apply(_, testee_header):
        assert_header_line_always_apply(testee_header, False)


class TestContent:  # ==========================================================

    def test_heading(_, testee_content):
        assert "## Coder CHANGELOG Writer" in testee_content

    def test_for_humans(_, testee_content):
        assert "- changelogs are *for humans*, not machines" in testee_content

    def test_every_version(_, testee_content):
        assert (
            "- there should be an entry for every single version"
            in testee_content
        )

    def test_unreleased_section(_, testee_content):
        assert "always maintain an `[Unreleased]` section" in testee_content

    def test_types_of_changes(_, testee_content):
        assert "**Types of Changes:**" in testee_content

    def test_type_added(_, testee_content):
        assert "- `Added`: new features" in testee_content

    def test_type_fixed(_, testee_content):
        assert "- `Fixed`: any bug fixes" in testee_content

    def test_format_title(_, testee_content):
        assert "- title must be `Project Name CHANGELOG`" in testee_content

    def test_format_links(_, testee_content):
        assert "- must include Github **links** at the end" in testee_content
