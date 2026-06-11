"""
cli-c-c-style-gw_test.py

Unit Tests (using pytest) for
"""

import pytest

from tests.cli import MD_FILENAME2SKILL_NAME
from tests.cli.c.c import (
    assert_rule_file_basic_format,
    split_rule_file_basic_format,
    assert_header_line_always_apply,
)

# constants  ###################################################################
MD_FILENAME = "style-guide-good-writing"
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
    return split_rule_file_basic_format(testee)[0]


@pytest.fixture(scope="session")
def testee_content(testee):
    return split_rule_file_basic_format(testee)[1]


# Pytest unit tests  ###########################################################


class TestBasic:  # ============================================================

    def test_existence(_, testee_path):
        assert testee_path.exists()

    def test_is_file(_, testee_path):
        assert testee_path.is_file()

    def test_structure(_, testee):
        assert assert_rule_file_basic_format(testee)


class TestHeader:  # ===========================================================

    def test_name(_, testee_header):
        name_line = "name: " + _SKILL_NAME
        assert name_line in testee_header

    def test_description(_, testee_header):
        assert (
            "description: explain Good Writing for general textual writing"
            in testee_header
        )

    def test_always_apply(_, testee_header):
        assert_header_line_always_apply(testee_header, False)


class TestContent:  # ==========================================================

    def test_heading(_, testee):
        assert "## Style Guide Good Writing" in testee

    def test_content0(_, testee):
        assert (
            "- Correct spelling, grammar, punctuation, sentence structure, and"
            " verb tense errors."
            in testee
        )

    def test_content1(_, testee):
        assert (
            "- Make only the minimum changes needed to improve correctness,"
            " readability, and clarity."
            in testee
        )

    def test_content2(_, testee):
        assert (
            "- Use American English by default, but if the original text"
            " clearly uses another spelling convention, preserve that"
            " convention."
            in testee
        )

    def test_content3(_, testee):
        assert "- Avoid generic filler when details are unavailable" in testee

    def test_content4(_, testee):
        assert (
            "- Avoid dense prose, generic filler, and unnecessary complexity"
            in testee
        )
