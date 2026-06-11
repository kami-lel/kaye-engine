"""
cli-c-c-style-brief_test.py

Unit Tests (using pytest) for:
"""

import pytest

from tests.cli import MD_FILENAME2SKILL_NAME
from tests.cli.c.c import (
    assert_rule_file_basic_format,
    split_rule_file_basic_format,
    assert_header_line_always_apply,
)

# constants  ###################################################################
MD_FILENAME = "style-guide-briefness-style"
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
            "description: "
            "explain Briefness Style on how to write concise content"
            in testee_header
        )

    def test_always_apply(_, testee_header):
        assert_header_line_always_apply(testee_header, False)


class TestContent:  # ==========================================================

    def test_heading(_, testee):
        assert "## Style Guide Briefness Style" in testee

    def test1(_, testee):
        assert (
            "- write in **newspaper headlinese**, "
            "prioritize brevity over grammar"
            in testee
        )

    def test2(_, testee):
        assert (
            "- omit articles (a, an, the) and helper verbs, "
            "use strong nouns, verbs"
            in testee
        )

    def test3(_, testee):
        assert (
            "- use numerals (use 2, not two), symbols, "
            "**Usable Abbrs** when unambiguous"
            in testee
        )

    def test4(_, testee):
        assert "- keep sentences short, direct, drop filler" in testee
