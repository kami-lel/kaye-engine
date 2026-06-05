"""
cli-ce-c-blueprint-style_test.py

Unit Tests (using pytest) for:

creation of ``style_blueprint.md``
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
    with open(testee_rules_folder / "style_blueprint.md") as f:
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
        assert "name: Style Guide" in testee_header

    def test_description(_, testee_header):
        assert (
            "description: writing tasks requiring house style and"
            " capitalization rules"
            in testee_header
        )

    def test_always_apply(_, testee_header):
        assert_header_line_always_apply(testee_header, False)


class TestContent:  # ==========================================================

    def test_title_case_heading(_, testee_content):
        assert "### Title Case" in testee_content

    def test_title_case_capitalize_major_words(_, testee_content):
        assert "- **capitalize major words**" in testee_content

    def test_title_case_lowercase_minor_words(_, testee_content):
        assert "- **lowercase minor words**" in testee_content

    def test_commentary_case_heading(_, testee_content):
        assert "### Commentary Case" in testee_content

    def test_commentary_case_first_sentence(_, testee_content):
        assert "- begin 1st sentence with a lowercase letter" in testee_content

    def test_briefness_style_heading(_, testee_content):
        assert "## Briefness Style" in testee_content

    def test_briefness_headlinese(_, testee_content):
        assert "- write in **newspaper headlinese**" in testee_content

    def test_good_writing_heading(_, testee_content):
        assert "## Good Writing" in testee_content

    def test_good_writing_spelling(_, testee_content):
        assert "- Correct spelling, grammar, punctuation" in testee_content

    def test_good_writing_american_english(_, testee_content):
        assert "- Use American English by default" in testee_content
