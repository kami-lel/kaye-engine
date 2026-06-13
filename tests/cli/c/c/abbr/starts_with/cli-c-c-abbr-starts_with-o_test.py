"""
cli-c-c-abbr-starts_with-o_test.py

Unit Tests (using pytest) for:

creation of ``abbr-starts_with-o``
"""

import pytest

from tests.cli import MD_FILENAME2SKILL_NAME
from tests.cli import (
    assert_frontmatter_md_file_basic_structure,
    split_frontmatter_md_file,
    assert_header_line_always_apply,
)

# constants  ###################################################################
MD_FILENAME = "abbr-starts-with-o"
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
        assert "name: Abbr Starts with O" in testee_header

    def test_always_apply(_, testee_header):
        assert_header_line_always_apply(testee_header, False)


class TestContent:  # ==========================================================

    def test_O(_, testee_content):
        assert "- O:only" in testee_content

    def test_obj(_, testee_content):
        assert "- obj:object" in testee_content

    def test_op(_, testee_content):
        assert "- op:operate,operation,operator" in testee_content

    def test_opmz(_, testee_content):
        assert "- opmz:optimize,optimization" in testee_content

    def test_opn_opinion(_, testee_content):
        assert "- opn:opinion" in testee_content

    def test_opp(_, testee_content):
        assert "- opp:oppose,opposition" in testee_content

    def test_opt(_, testee_content):
        assert "- opt:output" in testee_content

    def test_org(_, testee_content):
        assert "- org:organization" in testee_content

    def test_ori(_, testee_content):
        assert "- ori:origin,original" in testee_content

    def test_ot(_, testee_content):
        assert "- ot:other" in testee_content
