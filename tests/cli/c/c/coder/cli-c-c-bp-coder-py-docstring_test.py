"""
cli-c-c-bp-coder-py-docstring_test.py

Unit Tests (using pytest) for:

creation of ``Coder Python Docstring Style.md``
"""

import pytest

from tests.cli import MD_FILENAME2SKILL_NAME
from tests.cli import (
    assert_frontmatter_md_file_basic_structure,
    split_frontmatter_md_file,
    assert_header_line_always_apply,
)

# constants  ###################################################################
MD_FILENAME = "coder-python-docstring-style"
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
        assert "name: Coder Python Docstring Style" in testee_header

    def test_description(_, testee_header):
        assert (
            "Enforces a specific Python docstring convention: Sphinx style with reStructuredText markup"
            in testee_header[1]
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
