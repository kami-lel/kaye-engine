"""
cli-s-u-coder-js-ts_test.py

Unit Tests (using pytest) for:

creation of ``coder-javascript-and-typescript``
"""

import pytest

from tests.cli import (
    assert_frontmatter_md_file_basic_structure,
    split_frontmatter_md_file,
)
from tests.cli.s import (
    VERSION_LINE_PATTERN,
    convert_folder_path2skill_file_path,
)

# constants  ###################################################################


SKILL_NAME = "coder-javascript-and-typescript"


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
        assert "name: coder-javascript-and-typescript" in testee_header

    def test_description(_, testee_header):
        print(testee_header)
        assert (
            "description: Writes, edits, and reviews all JavaScript and"
            " TypeScript code, targeting the ES11 standard with camelCase"
            " naming and JSDoc documentation conventions."
            in testee_header
        )

    def test_when_to_use(_, testee_header):
        print(testee_header)
        assert (
            "when_to_use: 'Use for any JavaScript or TypeScript work."
            " Triggers: `.js`/`.ts`/`.jsx`/`.tsx` files, inline JS/TS"
            " code blocks, requests for JavaScript, TypeScript, or Node.'"
            in testee_header
        )

    def test_version(self, testee_header):
        assert any(VERSION_LINE_PATTERN.match(line) for line in testee_header)


class TestStructure:  # ========================================================

    def test_structure(_, testee_skill_file):
        assert assert_frontmatter_md_file_basic_structure(testee_skill_file)


class TestContent:  # ==========================================================

    def test_brace_style_heading(_, testee_content):
        assert "## Brace Style" in testee_content

    def test_brace_open(_, testee_content):
        assert "opening `{` on the **same line**" in testee_content

    def test_js_ts_heading(_, testee_content):
        assert "## Coder JavaScript and TypeScript" in testee_content

    def test_es11(_, testee_content):
        assert "**ES11** standard" in testee_content

    def test_naming_camelcase(_, testee_content):
        assert "Use **camelCase**" in testee_content

    def test_jsdoc(_, testee_content):
        assert "Use **JSDoc**" in testee_content
