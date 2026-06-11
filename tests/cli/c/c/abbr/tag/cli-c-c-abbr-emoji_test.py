"""
cli-c-c-abbr-emoji_test.py

Unit Tests (using pytest) for:

creation of ``abbr-emoji``
"""

import pytest

from tests.cli.c.c import (
    assert_rule_file_basic_format,
    split_rule_file_basic_format,
    assert_header_line_always_apply,
)

# Pytest fixtures  #############################################################


@pytest.fixture(scope="session")
def testee(testee_rules_folder):
    with open(testee_rules_folder / "Abbr Emoji.md") as f:
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
        assert "name: Abbr Emoji" in testee_header

    def test_always_apply(_, testee_header):
        assert_header_line_always_apply(testee_header, False)


class TestContent:  # ==========================================================

    def test_settings(_, testee_content):
        assert "- ⚙️:settings,preferences" in testee_content

    def test_warning(_, testee_content):
        assert "- ⚠️:warning" in testee_content

    def test_checkmark(_, testee_content):
        assert "- ✅:selected" in testee_content

    def test_correct(_, testee_content):
        assert "- ✔️:correct,correction" in testee_content

    def test_x_mark(_, testee_content):
        assert "- ❌:no,not,incorrect" in testee_content

    def test_finish(_, testee_content):
        assert "- 🏁:finish" in testee_content

    def test_bug(_, testee_content):
        assert "- 🐞:debug" in testee_content

    def test_lightbulb(_, testee_content):
        assert "- 💡:information,informational" in testee_content

    def test_explosion(_, testee_content):
        assert "- 💥:critical" in testee_content

    def test_chat(_, testee_content):
        assert "- 💬:chat,conversation" in testee_content

    def test_beginner(_, testee_content):
        assert "- 🔰:beginning,prototype" in testee_content

    def test_rocket(_, testee_content):
        assert "- 🚀:rapid,fast" in testee_content

    def test_stop(_, testee_content):
        assert "- 🛑:error" in testee_content

    def test_tools(_, testee_content):
        assert "- 🛠️:tools" in testee_content

    def test_robot(_, testee_content):
        assert "- 🤖:agent,AI" in testee_content
