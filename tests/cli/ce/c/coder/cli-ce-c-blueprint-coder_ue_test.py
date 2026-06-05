"""
cli-ce-c-blueprint-coder_ue_test.py

Unit Tests (using pytest) for:

creation of ``coder_ue_blueprint.md``
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
    with open(testee_rules_folder / "coder_ue_blueprint.md") as f:
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
        assert "name: Coder Unreal Engine" in testee_header

    def test_description(_, testee_header):
        assert "description: C++ code for Unreal Engine" in testee_header

    def test_globs(_, testee_header):
        assert 'globs: ["**/*.{cpp,cc,cxx,hpp,hh,hxx}"]' in testee_header

    def test_always_apply(_, testee_header):
        assert_header_line_always_apply(testee_header, False)


class TestContent:  # ==========================================================

    def test_brace_style_heading(_, testee_content):
        assert "## Brace Style" in testee_content

    def test_c_heading(_, testee_content):
        assert "## C" in testee_content

    def test_c99(_, testee_content):
        assert "Use **C99** standard" in testee_content

    def test_cpp_heading(_, testee_content):
        assert "## C++" in testee_content

    def test_cpp17(_, testee_content):
        assert "Use **C++17** standard" in testee_content

    def test_unreal_engine_heading(_, testee_content):
        assert "## Unreal Engine" in testee_content

    def test_unreal_version(_, testee_content):
        assert "Unreal Engine `5.6.0`" in testee_content
