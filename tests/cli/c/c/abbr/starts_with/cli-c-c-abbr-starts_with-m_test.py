"""
cli-c-c-abbr-starts_with-m_test.py

Unit Tests (using pytest) for:

creation of ``abbr-starts_with-m``
"""

import pytest

from tests.cli import MD_FILENAME2SKILL_NAME
from tests.cli import (
    assert_frontmatter_md_file_basic_structure,
    split_frontmatter_md_file,
    assert_header_line_always_apply,
)

# constants  ###################################################################
MD_FILENAME = "abbr-starts-with-m"
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
        assert "name: Abbr Starts with M" in testee_header

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
