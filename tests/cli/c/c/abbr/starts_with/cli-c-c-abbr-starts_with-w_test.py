"""
cli-c-c-abbr-starts_with-w_test.pw

Unit Tests (using pytest) for:

creation of ``abbr-starts_with-w``
"""

import pytest

from tests.cli import MD_FILENAME2SKILL_NAME
from tests.cli.c.c import (
    assert_rule_file_basic_format,
    split_rule_file_basic_format,
    assert_header_line_always_apply,
)

# constants  ###################################################################
MD_FILENAME = "abbr-starts-with-w"
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


class TestStructure:  # ========================================================

    def test_structure(_, testee):
        assert assert_rule_file_basic_format(testee)


class TestHeader:  # ===========================================================

    def test_name(_, testee_header):
        assert "name: Abbr Starts with W" in testee_header

    def test_always_apply(_, testee_header):
        assert_header_line_always_apply(testee_header, False)


class TestContent:  # ==========================================================

    def test_W_west(_, testee_content):
        assert "- W:west" in testee_content

    def test_w_with(_, testee_content):
        assert "- w/:with" in testee_content

    def test_w_within(_, testee_content):
        assert "- w/i:within" in testee_content

    def test_w_without(_, testee_content):
        assert "- w/o:without" in testee_content

    def test_wk(_, testee_content):
        assert "- wk:week" in testee_content

    def test_wl(_, testee_content):
        assert "- wl:would,will,willingness,willingly" in testee_content

    def test_wlx(_, testee_content):
        assert "- wlx:will/would not" in testee_content

    def test_wr(_, testee_content):
        assert "- wr:write" in testee_content

    def test_wt(_, testee_content):
        assert "- wt:want" in testee_content
