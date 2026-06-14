"""
cli-s-u-style-brief_test.py

Unit Tests (using pytest) for:

creation of ``style-guide-briefness-style``
"""

import pytest

from tests.cli import (
    assert_frontmatter_md_file_basic_structure,
    split_frontmatter_md_file,
)
from tests.cli.s import convert_folder_path2skill_file_path

# constants  ###################################################################


SKILL_NAME = "style-guide-briefness-style"


# Pytest fixtures  #############################################################


@pytest.fixture(scope="session")
def testee_folder(testee_skills_folder):
    return testee_skills_folder / SKILL_NAME


@pytest.fixture(scope="session")
def testee_skill_file_path(testee_folder):
    return convert_folder_path2skill_file_path(testee_folder)


@pytest.fixture(scope="session")
def testee_skill_file(testee_skill_file_path):
    with open(testee_skill_file_path) as f:
        return f.read()


@pytest.fixture(scope="session")
def testee_header(testee_skill_file):
    return split_frontmatter_md_file(testee_skill_file)[0]


@pytest.fixture(scope="session")
def testee_content(testee_skill_file):
    return split_frontmatter_md_file(testee_skill_file)[1]


# Pytest unit tests  ###########################################################


class TestBasic:  # ============================================================

    def test_existence(_, testee_skill_file_path):
        assert testee_skill_file_path.exists()

    def test_is_file(_, testee_skill_file_path):
        assert testee_skill_file_path.is_file()


class TestHeader:  # ===========================================================

    def test_name(_, testee_header):
        assert "name: style-guide-briefness-style" in testee_header

    def test_description(_, testee_header):
        print(testee_header)
        assert (
            'description: "Rewrites content in \\"Briefness Style\\" \\u2014'
            " terse, newspaper-headline prose that maximizes brevity: dropped"
            " articles and helper verbs, strong nouns and verbs, active voice,"
            " numerals and abbreviations, punctuation-compressed phrasing, no"
            ' terminal periods."'
            in testee_header
        )

    def test_when(_, testee_header):
        assert (
            'when_to_use: "Use when the user asks for headlinese, telegraphic,'
            " or ultra-condensed text \\u2014 notes, headlines, summaries,"
            ' bullets, status lines, captions \\u2014 or says \\"make it'
            ' brief/terse/punchy,\\" \\"cut words,\\" or \\"headline style.\\"'
            " Not for prose needing full grammar, formal tone, or complete"
            ' sentences."'
            in testee_header
        )


class TestStructure:  # ========================================================

    def test_structure(_, testee_skill_file):
        assert assert_frontmatter_md_file_basic_structure(testee_skill_file)


class TestContent:  # ==========================================================

    def test_heading(_, testee_content):
        assert "## Style Guide Briefness Style" in testee_content
