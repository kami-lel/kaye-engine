"""
cli-ce-c-blueprint-coder_project_test.py

Unit Tests (using pytest) for:

creation of ``coder_project_blueprint.md``
"""

import pytest

from tests.cli.ce.c import (
    assert_rule_file_basic_format,
    split_rule_file_basic_format,
    assert_header_line_always_apply,
)

# Pytest fixtures  #############################################################


@pytest.fixture(scope="session")
def testee(testee_rules_folder):
    with open(testee_rules_folder / "coder_project_blueprint.md") as f:
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
        assert "name: Project Structure" in testee_header

    def test_description(_, testee_header):
        assert (
            "description: generic Project/Repository structure for all"
            " programming languages"
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
