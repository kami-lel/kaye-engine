"""
cli-c-c-bp-coder-js-ts_test.py

Unit Tests (using pytest) for:

creation of ``coder_js_ts_blueprint.md``
"""

import pytest

from tests.cli.c.c import (
    assert_rule_file_basic_format,
    split_rule_file_basic_format,
    assert_header_line_always_apply,
)

# Pytest fixtures  #############################################################


@pytest.fixture(scope="session")
def testee(testee_rules_folder):
    with open(testee_rules_folder / "Coder JavaScript and TypeScript.md") as f:
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
        assert "name: Coder JavaScript and TypeScript" in testee_header

    def test_globs(_, testee_header):
        assert 'globs: ["**/*.{js,ts,jsx,tsx,mjs,cjs}"]' in testee_header

    def test_always_apply(_, testee_header):
        assert_header_line_always_apply(testee_header, False)


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
