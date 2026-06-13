"""
cli-c-c-abbr-programming_language_code_test.py

Unit Tests (using pytest) for:

creation of ``abbr-programming_language_code``
"""

import pytest

from tests.cli import MD_FILENAME2SKILL_NAME
from tests.cli import (
    assert_frontmatter_md_file_basic_structure,
    split_frontmatter_md_file,
    assert_header_line_always_apply,
)

# constants  ###################################################################
MD_FILENAME = "abbr-programming-language-codes"
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
        assert "name: Abbr Programming Language Codes" in testee_header

    def test_always_apply(_, testee_header):
        assert_header_line_always_apply(testee_header, False)


class TestContent:  # ==========================================================

    def test_bash(_, testee_content):
        assert "- bash:Bash" in testee_content

    def test_c(_, testee_content):
        assert "- c:C language" in testee_content

    def test_cpp(_, testee_content):
        assert "- cpp:C++" in testee_content

    def test_csharp(_, testee_content):
        assert "- csharp:C Sharp" in testee_content

    def test_gdscript(_, testee_content):
        assert "- gdscript:GDScript used by Godot Engine" in testee_content

    def test_js(_, testee_content):
        assert "- js:JavaScript" in testee_content

    def test_py(_, testee_content):
        assert "- py:Python" in testee_content

    def test_ts(_, testee_content):
        assert "- ts:TypeScript" in testee_content

    def test_u3d(_, testee_content):
        assert "- u3d:Unity Engine code" in testee_content

    def test_ue(_, testee_content):
        assert "- ue:Unreal Engine code" in testee_content
