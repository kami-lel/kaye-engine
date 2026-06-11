"""
cli-c-c-bp-coder-c_test.py

Unit Tests (using pytest) for:

creation of ``Coder C.md``
"""

import pytest

from tests.cli import MD_FILENAME2SKILL_NAME
from tests.cli.c.c import (
    assert_rule_file_basic_format,
    split_rule_file_basic_format,
    assert_header_line_always_apply,
)

# constants  ###################################################################
MD_FILENAME = "coder-c"
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
        assert "name: Coder C" in testee_header

    def test_description(_, testee_header):
        assert "description: C code (C99)" in testee_header

    def test_globs(_, testee_header):
        assert 'globs: ["**/*.{c,h}"]' in testee_header

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
