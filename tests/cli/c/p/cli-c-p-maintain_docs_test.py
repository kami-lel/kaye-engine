"""
cli-c-p-maintain_docs_test.py

Unit Tests (using pytest) for:

creation of ``maintain_docs.md``
"""

import pytest

from tests.cli import *  # noqa: F401, F403

# constants  ###################################################################
PROMPT_FILENAME = "maintain-docs"
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
        assert "## Maintain Docs" in testee_content

    def test_intro_docs_only(_, testee_content):
        assert "Update files under `docs/`." in testee_content

    def test_instructions_section(_, testee_content):
        assert "#### Instructions" in testee_content

    def test_instructions_review_changes(_, testee_content):
        assert "review recent repository changes" in testee_content

    def test_instructions_create_only_when_missing(_, testee_content):
        assert (
            "create new documentation only when an important expected file "
            "is missing or repository changes require it"
            in testee_content
        )

    def test_instructions_verify_content(_, testee_content):
        assert (
            "verify links, file paths, commands, configuration names, "
            "examples, and references where possible"
            in testee_content
        )

    def test_docs_files_section(_, testee_content):
        assert "#### Docs Files" in testee_content

    def test_docs_files_update_affected(_, testee_content):
        assert (
            "update affected APIs, commands, architecture notes, configuration "
            "details, examples, workflows, and troubleshooting guidance"
            in testee_content
        )

    def test_docs_files_cross_link(_, testee_content):
        assert (
            "cross-link related docs when it improves navigation"
            in testee_content
        )

    def test_output_section(_, testee_content):
        assert "#### Output" in testee_content
