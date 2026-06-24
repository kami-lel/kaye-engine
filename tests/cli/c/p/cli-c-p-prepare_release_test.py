"""
cli-c-p-prepare_release_test.py

Unit Tests (using pytest) for:

creation of ``prepare_for_release.md``
"""

import pytest

from tests.cli import *  # noqa: F401, F403

# constants  ###################################################################
PROMPT_FILENAME = "prepare-for-version-release"
_PROMPT_FILE = PROMPT_FILENAME2NAME[PROMPT_FILENAME]

# Pytest fixtures  #############################################################


@pytest.fixture(scope="session")
def testee_path(testee_prompts_folder):
    return testee_prompts_folder / (_PROMPT_FILE + ".md")


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

    def test_structure(_, testee):
        assert assert_frontmatter_md_file_basic_structure(testee)


class TestHeader:  # ===========================================================

    def test_name(_, testee_header):
        assert assert_continue_prompt_header_line_name(PROMPT_FILENAME, testee_header)

    def test_always_apply(_, testee_header):
        assert_header_line_always_apply(testee_header, False)

    def test_invokable(_, testee_header, header_invokable_line):
        assert header_invokable_line in testee_header


class TestContent:  # ==========================================================

    def test_heading(_, testee_content):
        assert "## Prepare for Version Release" in testee_content

    def test_intro_cut_release(_, testee_content):
        assert "Cut a new release: bring all docs current" in testee_content

    def test_preconditions_section(_, testee_content):
        assert "#### Preconditions" in testee_content

    def test_preconditions_require_version_and_date(_, testee_content):
        assert (
            "require both a version number and a release date; if either is"
            " missing"
            in testee_content
        )

    def test_steps_section(_, testee_content):
        assert "#### Steps" in testee_content

    def test_steps_sync_docs(_, testee_content):
        assert "**Sync the docs** to the state being released" in testee_content

    def test_steps_close_changelog(_, testee_content):
        assert "**Close out the changelog**" in testee_content

    def test_steps_bump_version(_, testee_content):
        assert "**Bump the project version**" in testee_content

    def test_output_section(_, testee_content):
        assert "#### Output" in testee_content
