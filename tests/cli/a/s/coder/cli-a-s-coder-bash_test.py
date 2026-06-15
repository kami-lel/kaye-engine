"""
cli-a-s-coder-bash_test.py

Unit Tests (using pytest) for:

creation of ``coder-bash``
"""

import pytest

from tests.cli import (
    TESTEE_FILE_CONTENT_ALL,
    assert_frontmatter_md_file_basic_structure,
    split_frontmatter_md_file,
)
from tests.cli.a.s import (
    VERSION_LINE_PATTERN,
    convert_folder_path2skill_file_path,
)

# constants  ###################################################################


SKILL_NAME = "coder-bash"
TESTEE_FILE_CONTENT = TESTEE_FILE_CONTENT_ALL[SKILL_NAME]


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
        assert "name: coder-bash" in testee_header

    def test_description(_, testee_header):
        print(testee_header)
        assert (
            'description: "Generates ready-to-run Debian GNU/Linux shell'
            " commands \\u2014 command-only output, sudo and destructive"
            ' commands when requested."'
            in testee_header
        )

    def test_when_to_use(_, testee_header):
        print(testee_header)
        assert (
            "when_to_use: 'Use for terminal commands or shell one-liners on"
            ' Debian/Ubuntu. Triggers: "command to...,"'
            ' "bash for...," CLI tasks.\''
            in testee_header
        )

    def test_version(self, testee_header):
        assert any(VERSION_LINE_PATTERN.match(line) for line in testee_header)


class TestStructure:  # ========================================================

    def test_structure(_, testee_skill_file):
        assert assert_frontmatter_md_file_basic_structure(testee_skill_file)


class TestContent:  # =========================================================

    def test0(_, testee_content):
        assert TESTEE_FILE_CONTENT[0] in testee_content

    def test1(_, testee_content):
        assert TESTEE_FILE_CONTENT[1] in testee_content

    def test2(_, testee_content):
        assert TESTEE_FILE_CONTENT[2] in testee_content

    def test3(_, testee_content):
        assert TESTEE_FILE_CONTENT[3] in testee_content

    def test4(_, testee_content):
        assert TESTEE_FILE_CONTENT[4] in testee_content

    def test5(_, testee_content):
        assert TESTEE_FILE_CONTENT[5] in testee_content