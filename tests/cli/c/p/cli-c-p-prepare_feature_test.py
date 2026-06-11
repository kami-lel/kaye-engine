"""
cli-c-p-prepare_feature_branch_finish_test.py

Unit Tests (using pytest) for:

creation of ``prepare_feature_branch_finish.md``
"""

import pytest

from tests.cli import PROMPT_FILENAME2NAME
from tests.cli.c.c import (
    assert_rule_file_basic_format,
    split_rule_file_basic_format,
    assert_header_line_always_apply,
)

# constants  ###################################################################
PROMPT_FILENAME = "prepare-for-feature"
_PROMPT_FILE = PROMPT_FILENAME2NAME[PROMPT_FILENAME]

# Pytest fixtures  #############################################################


@pytest.fixture(scope="session")
def testee_path(testee_prompts_folder):
    return testee_prompts_folder / _PROMPT_FILE


@pytest.fixture(scope="session")
def testee(testee_path):
    with open(testee_path) as f:
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
        assert "name: Prepare for Feature Finish" in testee_header

    def test_always_apply(_, testee_header):
        assert_header_line_always_apply(testee_header, False)

    def test_invokable(_, testee_header, header_invokable_line):
        assert header_invokable_line in testee_header


class TestContent:  # ==========================================================

    def test_heading(_, testee_content):
        assert "### Prepare for Feature Finish" in testee_content

    def test_intro_update_changelog(_, testee_content):
        assert "update `CHANGELOG.md`" in testee_content

    def test_add_relevant_changes(_, testee_content):
        assert (
            "add all relevant changes made by the current feature branch to "
            "the *Unreleased* section"
            in testee_content
        )

    def test_identify_feature_branch_changes(_, testee_content):
        assert "**identify feature branch changes**" in testee_content

    def test_identify_using_git_tools(_, testee_content):
        assert (
            "determine the changes by using available git tools"
            in testee_content
        )

    def test_preserve_existing_entries(_, testee_content):
        assert "**preserve existing changelog entries**" in testee_content

    def test_preserve_do_not_remove(_, testee_content):
        assert (
            "do not remove or overwrite existing entries in the "
            "*Unreleased* section"
            in testee_content
        )

    def test_avoid_duplicate_entries(_, testee_content):
        assert "**avoid duplicate entries**" in testee_content

    def test_avoid_duplicates_update_refine(_, testee_content):
        assert (
            "if some feature branch changes are already mentioned in the "
            "*Unreleased* section, update, refine, or reorganize them"
            in testee_content
        )

    def test_reorganize_when_helpful(_, testee_content):
        assert "**reorganize when helpful**" in testee_content

    def test_only_modify_changelog(_, testee_content):
        assert "**only modify `CHANGELOG.md`**" in testee_content

    def test_only_changelog_modification(_, testee_content):
        assert (
            "the only allowed file modification is `CHANGELOG.md`, and within "
            "that file, the only allowed content modification is inside the "
            "*Unreleased* section"
            in testee_content
        )
