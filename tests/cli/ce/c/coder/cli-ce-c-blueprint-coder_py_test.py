"""
cli-ce-c-blueprint-coder_py_test.py

Unit Tests (using pytest) for:

creation of ``coder_py_blueprint.md``
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
    with open(testee_rules_folder / "coder_py_blueprint.md") as f:
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
        assert "name: Coder Python" in testee_header

    def test_description(_, testee_header):
        assert "description: Python code" in testee_header

    def test_globs(_, testee_header):
        assert 'globs: ["**/*.py"]' in testee_header

    def test_always_apply(_, testee_header):
        assert_header_line_always_apply(testee_header, False)


class TestContent:  # ==========================================================

    def test_python_heading(_, testee_content):
        assert "## Python" in testee_content

    def test_pep8(_, testee_content):
        assert "Adhere to the **PEP8** style guide" in testee_content
