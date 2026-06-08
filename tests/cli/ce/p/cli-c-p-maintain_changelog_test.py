"""
cli-c-p-maintain_changelog_test.py

Unit Tests (using pytest) for:

creation of ``maintain_changelog.md``
"""

import pytest

from tests.cli.ce.c import (
    assert_rule_file_basic_format,
    split_rule_file_basic_format,
    assert_header_line_always_apply,
)

from tests.cli.ce.p import (
    assert_edit_changelog0,
    assert_edit_changelog1,
    assert_edit_changelog2,
)

# Pytest fixtures  #############################################################


@pytest.fixture(scope="session")
def testee(testee_prompts_folder):
    with open(testee_prompts_folder / "maintain_changelog.md") as f:
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
        assert "name: Maintain Changelog" in testee_header

    def test_always_apply(_, testee_header):
        assert_header_line_always_apply(testee_header, False)

    def test_invokable(_, testee_header, header_invokable_line):
        assert header_invokable_line in testee_header


class TestContent:  # ==========================================================

    def test_maintain_changelog_heading(_, testee_content):
        assert "### Maintain Changelog" in testee_content

    def test_review_recent_changes(_, testee_content):
        assert (
            "review recent changes — "
            "update or create `CHANGELOG.md` to reflect them."
            in testee_content
        )

    # edit CHANGELOG  ----------------------------------------------------------

    def test_edit_changelog0(_, testee_content):
        assert assert_edit_changelog0(testee_content)

    def test_edit_changelog1(_, testee_content):
        assert assert_edit_changelog1(testee_content)

    def test_edit_changelog2(_, testee_content):
        assert assert_edit_changelog2(testee_content)
