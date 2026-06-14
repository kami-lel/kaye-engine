"""
cli-c-c-bp-proj-ver_test.py

Unit Tests (using pytest) for:

creation of ``Project Semantic Versioning.md``
"""

import pytest

from tests.cli import MD_FILENAME2SKILL_NAME
from tests.cli import (
    assert_frontmatter_md_file_basic_structure,
    split_frontmatter_md_file,
    assert_header_line_always_apply,
)

# constants  ###################################################################
MD_FILENAME = "project-semantic-versioning"
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
        assert "name: Project Semantic Versioning" in testee_header

    def test_description(_, testee_header):
        assert any(
            line.startswith("description: ")
            and "Defines the project's semantic versioning scheme" in line
            for line in testee_header
        )

    def test_description_when_to_use(_, testee_header):
        assert any(
            line.startswith("description: ")
            and "Use when assigning, bumping, or formatting a version" in line
            for line in testee_header
        )

    def test_always_apply(_, testee_header):
        assert_header_line_always_apply(testee_header, False)


class TestContent:  # ==========================================================

    def test_heading(_, testee_content):
        assert "## Project Semantic Versioning" in testee_content

    def test_core_version_format(_, testee_content):
        assert "major.minor.patch" in testee_content

    def test_core_version_notation(_, testee_content):
        assert "x.y.z" in testee_content

    def test_prerelease_format(_, testee_content):
        assert "`x.y.z-alpha`, `x.y.z-alpha.2`" in testee_content

    def test_prerelease_character_set(_, testee_content):
        assert "[0-9a-z-]" in testee_content

    def test_build_metadata_example(_, testee_content):
        assert "`x.y.z+build.1`" in testee_content

    def test_build_character_set(_, testee_content):
        assert "[0-9A-Za-z-]" in testee_content

    def test_prerelease_types(_, testee_content):
        assert "pre-releases types: `alpha`, `beta`, `rc`" in testee_content

    def test_prerelease_numbering(_, testee_content):
        assert (
            "start at `.2`, e.g. `1.0.0-alpha.2`, `1.0.0-alpha.3`"
            in testee_content
        )

    def test_os_build_metadata(_, testee_content):
        assert "`1.0.0+Win`, `1.0.0+mac`, `1.0.0+linux`" in testee_content

    def test_development_stage_vertical_slice(_, testee_content):
        assert "vertical slice (VS): `0.5.z`~`0.8.z`" in testee_content

    def test_release_candidate_example(_, testee_content):
        assert "release candidate (RC): `1.0.0-rc`" in testee_content
