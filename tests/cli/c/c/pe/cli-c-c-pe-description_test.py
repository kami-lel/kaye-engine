"""
cli-c-c-pe-description_test.py

Unit Tests (using pytest) for:

creation of ``Skill Description Writer.md``
"""

import pytest

from tests.cli import MD_FILENAME2SKILL_NAME
from tests.cli import (
    assert_frontmatter_md_file_basic_structure,
    split_frontmatter_md_file,
    assert_header_line_always_apply,
)

# constants  ###################################################################
MD_FILENAME = "skill-description-writer"
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

    def test_structure(_, testee):
        assert assert_frontmatter_md_file_basic_structure(testee)


class TestHeader:  # ===========================================================

    def test_name(_, testee_header):
        name_line = "name: " + _SKILL_NAME
        assert name_line in testee_header

    def test_always_apply(_, testee_header):
        assert_header_line_always_apply(testee_header, False)


class TestContent:  # ==========================================================

    def test_heading(_, testee):
        assert "## Skill Description Writer" in testee

    def test1(_, testee):
        assert 'You are writing metadata for an agent "skill"' in testee

    def test2(_, testee):
        assert "a `description` and a `when_to_use`" in testee

    def test3(_, testee):
        assert "Keep both **concise and brief.**" in testee

    def test4(_, testee):
        assert (
            "**Always write in the third person, "
            "as a declarative statement of capability.**"
            in testee
        )

    def test5(_, testee):
        assert (
            "Quick test: a sentence describing the skill's capability"
            " belongs in `description`"
            in testee
        )
