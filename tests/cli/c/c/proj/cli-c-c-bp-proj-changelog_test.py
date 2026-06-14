"""
cli-c-c-bp-proj-changelog_test.py

Unit Tests (using pytest) for:

creation of ``Project CHANGELOG Writer.md``
"""

import pytest

from tests.cli import MD_FILENAME2SKILL_NAME
from tests.cli import (
    assert_frontmatter_md_file_basic_structure,
    split_frontmatter_md_file,
    assert_header_line_always_apply,
)

# constants  ###################################################################
MD_FILENAME = "project-changelog-writer"
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
        assert "name: Project CHANGELOG Writer" in testee_header

    def test_description(_, testee_header):
        print(testee_header)
        assert (
            'description: "Writes and maintains `CHANGELOG.md` files per'
            " Keep a Changelog conventions \\u2014 dated version entries"
            " newest-first, grouped change types, a persistent"
            " `[Unreleased]` section, and linkable version"
            " references.\\u21B5Use when creating, updating, or adding"
            " entries to a `CHANGELOG.md`, or recording changes for a"
            ' release. Triggers: \\"update the changelog,\\" \\"log this'
            ' change,\\" \\"document the release.\\""'
            in testee_header
        )

    def test_globs(_, testee_header):
        assert (
            'globs: ["**/{CHANGELOG,Changelog,changelog}{,.md,.txt}"]'
            in testee_header
        )

    def test_always_apply(_, testee_header):
        assert_header_line_always_apply(testee_header, False)


class TestContent:  # ==========================================================

    def test_heading(_, testee_content):
        assert "## Project CHANGELOG Writer" in testee_content

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
        assert (
            "- must include Github **links** at each section's end"
            in testee_content
        )
