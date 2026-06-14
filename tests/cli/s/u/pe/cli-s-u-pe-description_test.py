"""
cli-s-u-pe-description_test.py

Unit Tests (using pytest) for:

creation of ``skill-description-writer``
"""

import pytest

from tests.cli import (
    assert_frontmatter_md_file_basic_structure,
    split_frontmatter_md_file,
)
from tests.cli.s import convert_folder_path2skill_file_path

# constants  ###################################################################


SKILL_NAME = "skill-description-writer"


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
        assert "name: " + SKILL_NAME in testee_header


class TestStructure:  # ========================================================

    def test_structure(_, testee_skill_file):
        assert assert_frontmatter_md_file_basic_structure(testee_skill_file)


class TestContent:  # ==========================================================

    def test_heading(_, testee_content):
        assert "## Skill Description Writer" in testee_content

    def test1(_, testee_content):
        assert 'You are writing metadata for an agent "skill"' in testee_content

    def test2(_, testee_content):
        assert "a `description` and a `when_to_use`" in testee_content

    def test3(_, testee_content):
        assert "Keep both **extremely concise and brief**" in testee_content

    def test4(_, testee_content):
        assert (
            "**Always write in the third person, "
            "as a declarative statement of capability.**"
            in testee_content
        )

    def test5(_, testee_content):
        assert (
            "Quick test: a sentence describing the skill's capability"
            " belongs in `description`"
            in testee_content
        )
