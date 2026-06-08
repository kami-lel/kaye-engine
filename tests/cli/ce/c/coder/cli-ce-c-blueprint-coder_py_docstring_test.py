"""
cli-ce-c-blueprint-coder_py_docstring_test.py

Unit Tests (using pytest) for:

creation of ``Coder Python Docstring Style.md``
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
    with open(testee_rules_folder / "Coder Python Docstring Style.md") as f:
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
        assert "name: Coder Python Docstring Style" in testee_header

    def test_description(_, testee_header):
        assert (
            "description: Python docstrings in Sphinx/reStructuredText style"
            in testee_header
        )

    def test_globs(_, testee_header):
        assert 'globs: ["**/*.py"]' in testee_header

    def test_always_apply(_, testee_header):
        assert_header_line_always_apply(testee_header, False)


class TestContent:  # ==========================================================

    def test_docstring_style_heading(_, testee_content):
        assert "### Coder Python Docstring Style" in testee_content

    def test_sphinx_style(_, testee_content):
        assert "**Sphinx** style" in testee_content

    def test_restructuredtext(_, testee_content):
        assert "**reStructuredText**" in testee_content

    def test_public_methods(_, testee_content):
        assert (
            "- **public methods** must always include a docstring"
            in testee_content
        )

    def test_private_methods(_, testee_content):
        assert "- **private methods**" in testee_content

    def test_form_1(_, testee_content):
        assert "- *Form 1*" in testee_content

    def test_form_2(_, testee_content):
        assert "- *Form 2*" in testee_content

    def test_calc_square_example(_, testee_content):
        assert "def calc_square(number):" in testee_content

    def test_param_field(_, testee_content):
        assert ":param" in testee_content
