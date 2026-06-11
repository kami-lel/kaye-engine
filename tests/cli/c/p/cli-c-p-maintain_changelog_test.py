"""
cli-c-p-maintain_changelog_test.py

Unit Tests (using pytest) for:

creation of ``maintain_changelog.md``
"""

import pytest

from tests.cli import PROMPT_FILENAME2NAME
from tests.cli.c.c import (
    assert_rule_file_basic_format,
    split_rule_file_basic_format,
    assert_header_line_always_apply,
)

from tests.cli.c.p import (
    assert_edit_changelog0,
    assert_edit_changelog1,
    assert_edit_changelog2,
)

# constants  ###################################################################
PROMPT_FILENAME = "maintain-changelog"
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
        assert "name: Maintain CHANGELOG" in testee_header

    def test_always_apply(_, testee_header):
        assert_header_line_always_apply(testee_header, False)

    def test_invokable(_, testee_header, header_invokable_line):
        assert header_invokable_line in testee_header


class TestContent:  # ==========================================================

    def test_maintain_changelog_heading(_, testee_content):
        assert "### Maintain CHANGELOG" in testee_content

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
