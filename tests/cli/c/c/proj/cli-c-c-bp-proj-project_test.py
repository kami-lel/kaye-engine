"""
cli-c-c-bp-proj-project_test.py

Unit Tests (using pytest) for:

creation of ``Project Structure.md``
"""

import pytest

from tests.cli import MD_FILENAME2SKILL_NAME
from tests.cli import (
    assert_frontmatter_md_file_basic_structure,
    split_frontmatter_md_file,
    assert_header_line_always_apply,
)

# constants  ###################################################################
MD_FILENAME = "project-structure"
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
        assert "name: Project Structure" in testee_header

    def test_description(_, testee_header):
        print(testee_header)
        assert (
            'description: "Defines a standard, language-agnostic'
            " project/repository layout \\u2014 naming conventions and"
            " placement for top-level documentation files and source,"
            " build, docs, test, and tooling folders.\\u21B5Use when"
            " scaffolding a new repo, organizing an existing one, or"
            " deciding where a file or folder belongs. Triggers:"
            ' \\"set up project structure,\\" \\"where should this go,\\"'
            ' naming a standard doc or directory."'
            in testee_header
        )

    def test_always_apply(_, testee_header):
        assert_header_line_always_apply(testee_header, False)


class TestContent:  # ==========================================================

    def test_heading(_, testee_content):
        assert "## Project Structure" in testee_content

    def test_readme(_, testee_content):
        assert "- `README.md`:" in testee_content

    def test_changelog(_, testee_content):
        assert "- `CHANGELOG.md`:" in testee_content

    def test_agents(_, testee_content):
        assert "- `AGENTS.md`:" in testee_content

    def test_src(_, testee_content):
        assert "- `src/` or package-name:" in testee_content

    def test_tests(_, testee_content):
        assert "- `tests/`:" in testee_content

    def test_docs(_, testee_content):
        assert "- `docs/`:" in testee_content

    def test_scripts(_, testee_content):
        assert "- `scripts/`:" in testee_content
