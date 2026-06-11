"""
cli-c-c-abbr-starts_with-f_test.py

Unit Tests (using pytest) for:

creation of ``abbr-starts_with-f``
"""

import pytest

from tests.cli import MD_FILENAME2SKILL_NAME
from tests.cli.c.c import (
    assert_rule_file_basic_format,
    split_rule_file_basic_format,
    assert_header_line_always_apply,
)

# constants  ###################################################################
MD_FILENAME = "abbr-starts-with-f"
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


class TestStructure:  # ========================================================

    def test_structure(_, testee):
        assert assert_rule_file_basic_format(testee)


class TestHeader:  # ===========================================================

    def test_name(_, testee_header):
        assert "name: Abbr Starts with F" in testee_header

    def test_always_apply(_, testee_header):
        assert_header_line_always_apply(testee_header, False)


class TestContent:  # ==========================================================

    def test_F_fall(_, testee_content):
        assert "- F:fall" in testee_content

    def test_F_false(_, testee_content):
        assert "- F:false" in testee_content

    def test_fd(_, testee_content):
        assert "- fd:find,found" in testee_content

    def test_fm(_, testee_content):
        assert "- fm:formal" in testee_content

    def test_fmt(_, testee_content):
        assert "- fmt:format,formatting" in testee_content

    def test_fr(_, testee_content):
        assert "- fr:from" in testee_content

    def test_frq(_, testee_content):
        assert "- frq:frequent,frequently,frequency" in testee_content

    def test_fx(_, testee_content):
        assert "- fx:function" in testee_content
