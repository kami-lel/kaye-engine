"""
cli-c-c-bp-coder-py-testing_test.py

Unit Tests (using pytest) for:

creation of ``coder_py_testing_blueprint.md``
"""

import pytest

from tests.cli import MD_FILENAME2SKILL_NAME
from tests.cli import (
    assert_frontmatter_md_file_basic_structure,
    split_frontmatter_md_file,
    assert_header_line_always_apply,
)

# constants  ###################################################################
MD_FILENAME = "coder-python-testing-guidelines"
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
