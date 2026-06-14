"""
cli-c-c-bp-coder-bash_test.py

Unit Tests (using pytest) for:

creation of ``coder_bash_blueprint.md``
"""

import pytest

from tests.cli import MD_FILENAME2SKILL_NAME
from tests.cli import (
    assert_frontmatter_md_file_basic_structure,
    split_frontmatter_md_file,
    assert_header_line_always_apply,
)

# constants  ###################################################################
MD_FILENAME = "coder-bash"
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
        assert "name: Coder Bash" in testee_header

    def test_description(_, testee_header):
        print(testee_header)
        assert (
            'description: "Generates ready-to-run Debian GNU/Linux shell'
            ' commands \\u2014 command-only output, sudo and destructive'
            ' commands when requested.\\u21B5Use for terminal commands or'
            ' shell one-liners on Debian/Ubuntu. Triggers: \\"command'
            ' to...,\\" \\"bash for...,\\" CLI tasks."'
            in testee_header
        )

    def test_always_apply(_, testee_header):
        assert_header_line_always_apply(testee_header, False)


class TestContent:  # ==========================================================

    def test_heading(_, testee_content):
        assert "## Coder Bash" in testee_content

    def test_debian_only(_, testee_content):
        assert "Debian GNU/Linux only" in testee_content

    def test_gnu_tools(_, testee_content):
        assert "Use standard GNU and Debian tools only." in testee_content

    def test_no_explanation(_, testee_content):
        assert (
            "Return only the command or commands, with no explanation."
            in testee_content
        )

    def test_sudo(_, testee_content):
        assert "Use sudo when needed." in testee_content

    def test_clarifying_question(_, testee_content):
        assert "ask one short clarifying question" in testee_content
