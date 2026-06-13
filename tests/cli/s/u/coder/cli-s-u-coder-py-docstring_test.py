"""
cli-s-u-coder-py-docstring_test.py

Unit Tests (using pytest) for:

creation of ``coder-python-docstring-style``
"""

import pytest

from tests.cli import (
    assert_frontmatter_md_file_basic_structure,
    split_frontmatter_md_file,
)
from tests.cli.s import convert_folder_path2skill_file_path

# constants  ###################################################################


SKILL_NAME = "coder-python-docstring-style"


# Pytest fixtures  #############################################################


@pytest.fixture(scope="session")
def testee_folder(testee_skills_folder):
    return testee_skills_folder / SKILL_NAME


@pytest.fixture(scope="session")
def testee_skill_file_path(testee_folder):
    return convert_folder_path2skill_file_path(testee_folder)


@pytest.fixture(scope="session")
def testee_skill_file(testee_skill_file_path):
    with open(testee_skill_file_path) as f:
        return f.read()


@pytest.fixture(scope="session")
def testee_header(testee_skill_file):
    return split_frontmatter_md_file(testee_skill_file)[0]


@pytest.fixture(scope="session")
def testee_content(testee_skill_file):
    return split_frontmatter_md_file(testee_skill_file)[1]


# Pytest unit tests  ###########################################################


class TestBasic:  # ============================================================

    def test_existence(_, testee_skill_file_path):
        assert testee_skill_file_path.exists()

    def test_is_file(_, testee_skill_file_path):
        assert testee_skill_file_path.is_file()


class TestHeader:  # ===========================================================

    def test_name(_, testee_header):
        assert "name: coder-python-docstring-style" in testee_header

    def test_description(_, testee_header):
        assert any(
            'description: "Enforces a specific Python docstring convention:'
            in line
            for line in testee_header
        )


class TestStructure:  # ========================================================

    def test_structure(_, testee_skill_file):
        assert assert_frontmatter_md_file_basic_structure(testee_skill_file)


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
