"""
cli-a-u-chat_test.py

Unit Tests (using pytest) for:

kaye claude user-system-prompt
"""

import subprocess

import pytest

# TODO fuller unit test for CLI a u


# constants  ###################################################################


SKILL_NAME = "chat"
TESTEE_FILE_CONTENT = [
    "# Introduction",
    "# Personality",
    "# Language",
    "# Style Guide",
    "## Style Guide Markdown Format",
    "#### List Format",
    "#### Math Formatting",
    "#### Diagrams",
    "# Role",
    "- must use blockquote `>` for your emotions",
    "- always respond in the **same language**",
]


# Pytest fixtures  #############################################################


@pytest.fixture(scope="session")
def testee_claude_md_file_path(tmp_path_factory, cli_claude_command):
    tmp_folder = tmp_path_factory.mktemp("claude_user_prompt")
    claude_md_path = tmp_folder / "CLAUDE.md"

    cmd = cli_claude_command + "user-system-prompt " + str(claude_md_path)
    subprocess.run(cmd, shell=True, check=True)

    return claude_md_path


@pytest.fixture(scope="session")
def testee_content(testee_claude_md_file_path):
    with open(testee_claude_md_file_path) as f:
        return f.read()


# Pytest unit tests  ###########################################################


class TestBasic:  # ============================================================

    def test_existence(_, testee_claude_md_file_path):
        assert testee_claude_md_file_path.exists()

    def test_is_file(_, testee_claude_md_file_path):
        assert testee_claude_md_file_path.is_file()


class TestContent:  # ==========================================================

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

    def test6(_, testee_content):
        assert TESTEE_FILE_CONTENT[6] in testee_content

    def test7(_, testee_content):
        assert TESTEE_FILE_CONTENT[7] in testee_content

    def test8(_, testee_content):
        assert TESTEE_FILE_CONTENT[8] in testee_content

    def test9(_, testee_content):
        assert TESTEE_FILE_CONTENT[9] in testee_content
