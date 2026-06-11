"""
cli-c-c-abbr-prefix_test.py

Unit Tests (using pytest) for:

creation of ``abbr-prefix``
"""

import pytest

from tests.cli import MD_FILENAME2SKILL_NAME
from tests.cli.c.c import (
    assert_rule_file_basic_format,
    split_rule_file_basic_format,
    assert_header_line_always_apply,
)

# constants  ###################################################################
MD_FILENAME = "abbr-prefixes"
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
        assert "name: Abbr Prefixes" in testee_header

    def test_always_apply(_, testee_header):
        assert_header_line_always_apply(testee_header, False)


class TestContent:  # ==========================================================

    def test_a_an(_, testee_content):
        assert "- a.:an-" in testee_content

    def test_a_anti(_, testee_content):
        assert "- a.:anti-" in testee_content

    def test_c_co(_, testee_content):
        assert "- c.:co-" in testee_content

    def test_d_de(_, testee_content):
        assert "- d.:de-" in testee_content

    def test_i(_, testee_content):
        assert "- i.:in-,inter-" in testee_content

    def test_m(_, testee_content):
        assert "- m.:mal-" in testee_content

    def test_n(_, testee_content):
        assert "- n.:non-" in testee_content

    def test_o(_, testee_content):
        assert "- o.:over-" in testee_content

    def test_p(_, testee_content):
        assert "- p.:pro-" in testee_content

    def test_u(_, testee_content):
        assert "- u.:un-" in testee_content
