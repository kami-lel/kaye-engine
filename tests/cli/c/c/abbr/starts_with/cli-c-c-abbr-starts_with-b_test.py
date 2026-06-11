"""
cli-c-c-abbr-starts_with-b_test.py

Unit Tests (using pytest) for:

creation of ``abbr-starts_with-b``
"""

import pytest

from tests.cli import MD_FILENAME2SKILL_NAME
from tests.cli.c.c import (
    assert_rule_file_basic_format,
    split_rule_file_basic_format,
    assert_header_line_always_apply,
)

# constants  ###################################################################
MD_FILENAME = "abbr-starts-with-b"
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
        assert "name: Abbr Starts with B" in testee_header

    def test_always_apply(_, testee_header):
        assert_header_line_always_apply(testee_header, False)


class TestContent:  # ==========================================================

    def test_B(_, testee_content):
        assert "- B:but,however" in testee_content

    def test_b_bad(_, testee_content):
        assert "- b.:bad" in testee_content

    def test_b_c(_, testee_content):
        assert "- b/c:because,caused by,result of" in testee_content

    def test_b_t(_, testee_content):
        assert "- b/t:between" in testee_content

    def test_b4(_, testee_content):
        assert "- b4:before" in testee_content

    def test_bc(_, testee_content):
        assert (
            "- BC:before Christ,before common era,used after year number"
            in testee_content
        )

    def test_bg(_, testee_content):
        assert "- bg:background" in testee_content

    def test_bk(_, testee_content):
        assert "- bk:book" in testee_content

    def test_bb(_, testee_content):
        assert "- bb:worse" in testee_content

    def test_bx(_, testee_content):
        assert "- bx:worst" in testee_content
