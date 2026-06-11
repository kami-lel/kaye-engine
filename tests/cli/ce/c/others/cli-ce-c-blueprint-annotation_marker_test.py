"""
cli-ce-c-blueprint-annotation_marker_test.py

Unit Tests (using pytest) for:

creation of ``Annotation Markers.md``
"""

import pytest

from tests.cli import MD_FILENAME2SKILL_NAME
from tests.cli.ce.c import (
    assert_rule_file_basic_format,
    split_rule_file_basic_format,
    assert_header_line_always_apply,
)

# constants  ###################################################################
MD_FILENAME = "annotation-markers"
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
        assert "name: Annotation Markers" in testee_header

    def test_description(_, testee_header):
        assert (
            "description: when working with BUG, FIXME, TODO,"
            " or HACK markers in code or docs"
            in testee_header
        )

    def test_always_apply(_, testee_header):
        assert_header_line_always_apply(testee_header, False)


class TestContent:  # ==========================================================

    def test_heading(_, testee_content):
        assert "## Annotation Markers" in testee_content

    def test_primary_am(_, testee_content):
        assert "- primary AM: BUG, FIXME, TODO, HACK" in testee_content

    def test_secondary_am(_, testee_content):
        assert "- secondary AM: Bug, Fixme, Todo, Hack" in testee_content

    def test_tertiary_am(_, testee_content):
        assert "- tertiary AM: bug, fixme, todo, hack" in testee_content

    def test_promote_demote(_, testee_content):
        assert "call it **promote**" in testee_content

    def test_meaning_heading(_, testee_content):
        assert "### Meaning" in testee_content

    def test_meaning_bug(_, testee_content):
        assert "- BUG/Bug/bug:" in testee_content

    def test_meaning_todo(_, testee_content):
        assert "- todo/..." in testee_content

    def test_no_modify_rule(_, testee_content):
        assert "- do not modify or remove any markers unless" in testee_content
