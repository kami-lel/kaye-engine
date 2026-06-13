"""
cli-c-c-bp-coder-cpp_test.py

Unit Tests (using pytest) for:

creation of ``coder_cpp_blueprint.md``
"""

import pytest

from tests.cli import MD_FILENAME2SKILL_NAME
from tests.cli import (
    assert_frontmatter_md_file_basic_structure,
    split_frontmatter_md_file,
    assert_header_line_always_apply,
)

# constants  ###################################################################
MD_FILENAME = "coder-cpp"
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
        assert "name: Coder CPP" in testee_header

    def test_description(_, testee_header):
        assert "description: C++ code (C++17)" in testee_header

    def test_globs(_, testee_header):
        assert 'globs: ["**/*.{cpp,cc,cxx,hpp,hh,hxx}"]' in testee_header

    def test_always_apply(_, testee_header):
        assert_header_line_always_apply(testee_header, False)


class TestContent:  # ==========================================================

    def test_brace_style_heading(_, testee_content):
        assert "## Brace Style" in testee_content

    def test_brace_open(_, testee_content):
        assert "opening `{` on the **same line**" in testee_content

    def test_brace_close(_, testee_content):
        assert "closing `}` on its **own line**" in testee_content

    def test_c_heading(_, testee_content):
        assert "## Coder C" in testee_content

    def test_c99(_, testee_content):
        assert "Use **C99** standard" in testee_content

    def test_cpp_heading(_, testee_content):
        assert "## Coder CPP" in testee_content

    def test_cpp17(_, testee_content):
        assert "Use **C++17** standard" in testee_content
