"""
cli-c-c-bp-coder-csharp_test.py

Unit Tests (using pytest) for:

creation of ``coder_csharp_blueprint.md``
"""

import pytest

from tests.cli import *  # noqa: F401, F403

# constants  ###################################################################
MD_FILENAME = "coder-c-sharp"
TESTEE_FILE_CONTENT = TESTEE_FILE_CONTENT_ALL[MD_FILENAME]
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
        assert assert_continue_blueprint_header_line_name(MD_FILENAME, testee_header)

    def test_description(_, testee_header):
        assert assert_description_in_continue_description_field(MD_FILENAME, testee_header)

    def test_when_to_use(_, testee_header):
        assert assert_when_to_use_in_continue_description_field(MD_FILENAME, testee_header)

    def test_globs(_, testee_header):
        assert 'globs: ["**/*.cs"]' in testee_header

    def test_always_apply(_, testee_header):
        assert_header_line_always_apply(testee_header, False)


class TestContent:  # =========================================================

    @pytest.mark.parametrize("i", range(len(TESTEE_FILE_CONTENT)))
    def test_content(_, testee_content, i):
        assert TESTEE_FILE_CONTENT[i] in testee_content
