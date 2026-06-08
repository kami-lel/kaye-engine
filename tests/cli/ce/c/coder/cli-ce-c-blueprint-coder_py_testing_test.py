"""
cli-ce-c-blueprint-coder_py_testing_test.py

Unit Tests (using pytest) for:

creation of ``coder_py_testing_blueprint.md``
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
    with open(testee_rules_folder / "coder_py_testing_blueprint.md") as f:
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
        assert "name: Coder Python Testing Guidelines" in testee_header

    def test_description(_, testee_header):
        assert (
            "description: Python tests using pytest with Test classes and"
            " test_ functions"
            in testee_header
        )

    def test_globs(_, testee_header):
        assert 'globs: ["**/test_*.py", "**/*_test.py"]' in testee_header

    def test_always_apply(_, testee_header):
        assert_header_line_always_apply(testee_header, False)


class TestContent:  # ==========================================================

    def test_testing_guidelines_heading(_, testee_content):
        assert "### Coder Python Testing Guidelines" in testee_content

    def test_pytest_mention(_, testee_content):
        assert "`pytest` module" in testee_content

    def test_test_class_names(_, testee_content):
        assert "test class names should start with `Test`" in testee_content

    def test_test_function_names(_, testee_content):
        assert "test function names should begin with `test_`" in testee_content

    def test_separate_test_functions(_, testee_content):
        assert (
            "strive to create as many separate test functions" in testee_content
        )

    def test_no_docstrings(_, testee_content):
        assert "do **not** require docstrings" in testee_content

    def test_module_docstring(_, testee_content):
        assert "**Each test file**" in testee_content

    def test_math_utils_example(_, testee_content):
        assert "TestAdd" in testee_content

    def test_test_add_class(_, testee_content):
        assert "class TestAdd:" in testee_content
