"""
cli-ce-c-abbr-starts_with-m_test.py

Unit Tests (using pytest) for:

creation of ``abbr-starts_with-m``
"""

import pytest

from tests.cli.ce.c import (
    assert_rule_file_basic_format,
    split_rule_file_basic_format,
    assert_header_line_always_apply,
)

# Pytest fixtures  #############################################################


@pytest.fixture(scope="session")
def testee(testee_rules_folder):
    with open(testee_rules_folder / "abbr-starts_with-m.md") as f:
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
        assert "name: Abbreviations Starts with M" in testee_header

    def test_always_apply(_, testee_header):
        assert_header_line_always_apply(testee_header, False)


class TestContent:  # ==========================================================

    def test_M(_, testee_content):
        assert "- M:must" in testee_content

    def test_max(_, testee_content):
        assert "- max:maximum,maximize,maximization" in testee_content

    def test_min(_, testee_content):
        assert "- min:minimum,minimize,minimization" in testee_content

    def test_mk(_, testee_content):
        assert "- mk:make" in testee_content

    def test_mpl(_, testee_content):
        assert "- mpl:implement" in testee_content

    def test_mpt(_, testee_content):
        assert "- mpt:important,importance" in testee_content

    def test_mpv(_, testee_content):
        assert "- mpv:improve,improvement" in testee_content

    def test_mthd(_, testee_content):
        assert "- mthd:method" in testee_content

    def test_mv(_, testee_content):
        assert "- mv:move" in testee_content

    def test_Mx(_, testee_content):
        assert "- Mx:must not" in testee_content
