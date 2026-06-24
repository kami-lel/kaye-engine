"""
cli-c-p-prepare_feature_branch_finish_test.py

Unit Tests (using pytest) for:

creation of ``prepare_feature_branch_finish.md``
"""

import pytest

from tests.cli import *  # noqa: F401, F403

# constants  ###################################################################
PROMPT_FILENAME = "prepare-for-feature"
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
        assert "## Prepare for Feature Finish" in testee_content

    def test_intro_sync_docs(_, testee_content):
        assert "Before merging the current feature branch" in testee_content

    def test_instructions_section(_, testee_content):
        assert "#### Instructions" in testee_content

    def test_instructions_identify_changes(_, testee_content):
        assert (
            "identify this branch's changes once" in testee_content
        )

    def test_instructions_maintain_changelog(_, testee_content):
        assert "**Maintain CHANGELOG** → record the branch's changes" in testee_content

    def test_instructions_maintain_agents(_, testee_content):
        assert "**Maintain AGENTS and CONTEXT** → update them for any" in testee_content

    def test_output_section(_, testee_content):
        assert "#### Output" in testee_content
