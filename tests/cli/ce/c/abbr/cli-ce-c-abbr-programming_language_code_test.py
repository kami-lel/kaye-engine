"""
cli-ce-c-abbr-programming_language_code_test.py

Unit Tests (using pytest) for:

creation of ``abbr-programming_language_code``
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
    with open(
        testee_rules_folder / "abbr-programming_language_code.md"
    ) as f:
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
        assert (
            "name: Abbreviations Programming Language Codes"
            in testee_header
        )

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
