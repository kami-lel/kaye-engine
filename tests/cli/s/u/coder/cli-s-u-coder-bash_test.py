"""
cli-s-u-coder-bash_test.py

Unit Tests (using pytest) for:

creation of ``coder-bash``
"""

import pytest

from tests.cli import (
    assert_frontmatter_md_file_basic_structure,
    split_frontmatter_md_file,
)
from tests.cli.s import convert_folder_path2skill_file_path

# constants  ###################################################################


SKILL_NAME = "coder-bash"


# Pytest fixtures  #############################################################


@pytest.fixture(scope="session")
def testee_folder(testee_skills_folder):
    return testee_skills_folder / SKILL_NAME


@pytest.fixture(scope="session")
def testee_skill_file_path(testee_folder):
    return convert_folder_path2skill_file_path(testee_folder)


@pytest.fixture(scope="session")
def testee_skill_file(testee_skill_file_path):
    with open(testee_skill_file_path) as f:
        return f.read()


@pytest.fixture(scope="session")
def testee_header(testee_skill_file):
    return split_frontmatter_md_file(testee_skill_file)[0]


@pytest.fixture(scope="session")
def testee_content(testee_skill_file):
    return split_frontmatter_md_file(testee_skill_file)[1]


# Pytest unit tests  ###########################################################


class TestBasic:  # ============================================================

    def test_existence(_, testee_skill_file_path):
        assert testee_skill_file_path.exists()

    def test_is_file(_, testee_skill_file_path):
        assert testee_skill_file_path.is_file()


class TestHeader:  # ===========================================================

    def test_name(_, testee_header):
        assert "name: coder-bash" in testee_header

    def test_description(_, testee_header):
        assert (
            "description: Debian GNU/Linux shell commands; ready-to-run output"
            in testee_header
        )


class TestStructure:  # ========================================================

    def test_structure(_, testee_skill_file):
        assert assert_frontmatter_md_file_basic_structure(testee_skill_file)


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
