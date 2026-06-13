"""
cli-s-u-coder-u3d_test.py

Unit Tests (using pytest) for:

creation of ``coder-unity-engine``
"""

import pytest

from tests.cli import (
    assert_frontmatter_md_file_basic_structure,
    split_frontmatter_md_file,
)
from tests.cli.s import convert_folder_path2skill_file_path

# constants  ###################################################################


SKILL_NAME = "coder-unity-engine"


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
        assert "name: coder-unity-engine" in testee_header

    def test_description(_, testee_header):
        assert (
            "description: C# code for Unity 6 (MonoBehaviour scripts,"
            " components, Inspector fields)"
            in testee_header
        )


class TestStructure:  # ========================================================

    def test_structure(_, testee_skill_file):
        assert assert_frontmatter_md_file_basic_structure(testee_skill_file)


class TestContent:  # ==========================================================

    def test_brace_style_heading(_, testee_content):
        assert "## Brace Style" in testee_content

    def test_csharp_heading(_, testee_content):
        assert "## Coder C Sharp" in testee_content

    def test_unity_engine_heading(_, testee_content):
        assert "## Coder Unity Engine" in testee_content

    def test_unity_version(_, testee_content):
        assert "Unity **6**" in testee_content

    def test_monobehaviour_heading(_, testee_content):
        assert "### MonoBehaviour" in testee_content

    def test_section_ordering(_, testee_content):
        assert "- **section order is fixed**" in testee_content

    def test_public_members(_, testee_content):
        assert "// Public Members" in testee_content

    def test_inspector_fields(_, testee_content):
        assert "// Inspector Fields" in testee_content

    def test_inspector_guard_heading(_, testee_content):
        assert "#### Inspector Assignment Guard" in testee_content
